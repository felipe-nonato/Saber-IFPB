from api.database import db
from api.models.book import Book
from api.models.user import User
from api.models.rental import Rental
from api.models.penalty import Penalty
from api.patterns.pricing_strategy import PrecificacaoStrategy
from api.patterns.singleton import SistemaEconomia
from api.patterns.observer import Subject  # Para o subject de notificação
from api.config import Configuration
import datetime


class BibliotecaMediator:
    def __init__(
        self,
        db_instance,
        pricing_strategy: PrecificacaoStrategy,
        sistema_economia: SistemaEconomia,
        notification_subject: Subject,
    ):
        self.db = db_instance
        self.pricing_strategy = pricing_strategy
        self.sistema_economia = sistema_economia
        self.notification_subject = notification_subject
        self.config = Configuration()  # Acessa a configuração

    def processarDeposito(self, book, depositor):
        deposit_coins = self.pricing_strategy.calcularPrecoDeposito()

    def processarAluguel(self, book_id: str, user_id: int):
        book = Book.query.get(book_id)
        user = User.query.get(user_id)

        if not book:
            return None, "Livro não encontrado."
        if not user:
            return None, "Usuário não encontrado."

        # Delega ao estado do livro para lidar com a lógica de aluguel
        # O objeto de estado chamará de volta o mediador para operações complexas.
        try:
            return book.estado.alugar(
                user, self
            )  # Passa a instância do mediador para o estado
        except ValueError as e:
            self.db.session.rollback()  # Garante rollback em caso de falha de validação
            return None, str(e)
        except Exception as e:
            self.db.session.rollback()
            return None, f"Erro inesperado ao processar aluguel: {str(e)}"

    def _execute_rental(self, book: Book, user: User):
        """Método interno para completar o processo de aluguel após a validação do estado."""
        rent_cost = self.pricing_strategy.calcularPrecoAluguel(
            self.config.RENTAL_PERIOD_DAYS
        )
        if not user.diminuirMoedas(rent_cost):
            raise ValueError(f"Usuário {user.nome} não tem {rent_cost} moedas suficientes para alugar o livro {book.titulo}.")

        # Atualiza o estado do livro e os detalhes
        book.alterarEstado("alugado")  # Define o estado como string
        book.rentee_id = user.id

        rental_start_date = datetime.datetime.utcnow()
        rental_end_date = rental_start_date + datetime.timedelta(
            days=self.config.RENTAL_PERIOD_DAYS
        )

        # Cria um registro histórico de aluguel
        new_rental = Rental(
            book_id=book.id,
            rentee_id=user.id,
            preco=rent_cost,
            data_aluguel=rental_start_date,
            data_devolucao=rental_end_date,
        )
        self.db.session.add(new_rental)

        # Repassa moedas para o depositante via SistemaEconomia
        depositor = User.query.get(book.depositor_id)
        system_user = User.query.filter_by(nome="system").first()
        system_user_id = system_user.id if system_user else 0

        if depositor:
            self.sistema_economia.repassarMoedas(user.id, depositor.id, rent_cost)
            # Notifica o depositante sobre moedas recebidas
            self.notification_subject.notify(
                "coin_received", user=depositor, amount=rent_cost, source_user=user
            )
        else:
            print(
                f"Depositante do livro {book.titulo} não encontrado para repassar moedas."
            )
            self.sistema_economia.repassarMoedas(
                user.id, system_user_id, rent_cost
            )  # Repassa para o sistema se não houver depositante

        self.db.session.commit()
        self.notification_subject.notify(
            "book_rented", book=book, user=user, due_date=rental_end_date
        )
        return book, "Livro alugado com sucesso."

    def processarDevolucao(self, book_id: str, user_id: int):
        book = Book.query.get(book_id)
        user = User.query.get(user_id)

        if not book:
            return None, "Livro não encontrado."
        if not user:
            return None, "Usuário não encontrado."

        try:
            return book.estado.devolver(
                user, self
            )  # Passa a instância do mediador para o estado
        except ValueError as e:
            self.db.session.rollback()
            return None, str(e)
        except Exception as e:
            self.db.session.rollback()
            return None, f"Erro inesperado ao processar devolução: {str(e)}"

    def _execute_return(self, book: Book, user: User):
        """Método interno para completar o processo de devolução após a validação do estado."""
        # Calcula penalidade se estiver atrasado
        self.calcularPenalizacao(book, user)

        # Atualiza o estado do livro e os detalhes
        book.rentee_id = None  # Limpa o locatário atual

        # Encontra o último registro de aluguel ativo para este livro e usuário e atualiza a data de devolução
        latest_rental = (
            Rental.query.filter_by(
                book_id=book.id, rentee_id=user.id, dataDevolucao=None
            )
            .order_by(Rental.dataAluguel.desc())
            .first()
        )
        if latest_rental:
            latest_rental.dataDevolucao = datetime.datetime.utcnow()
            self.db.session.add(latest_rental)

        # Verifica por reserva e notifica o próximo usuário
        if book.reserved_by_id:
            reserved_user = User.query.get(book.reserved_by_id)
            if reserved_user:
                book.alterarEstado(
                    "reservado"
                )  # Livro agora reservado para o próximo usuário
                self.notification_subject.notify(
                    "book_reserved", book=book, user=reserved_user
                )
            else:
                book.reserved_by_id = None  # Limpa reserva inválida
                book.alterarEstado("disponivel")
        else:
            book.alterarEstado("disponivel")  # Nenhuma reserva, torna-se disponível

        self.db.session.commit()
        self.notification_subject.notify("book_returned", book=book, user=user)
        return book, "Livro devolvido com sucesso."

    def processarDeposito(self, book: Book, depositor: User):
        system_user = User.query.filter_by(nome="system").first()
        if not system_user:
            return (
                None,
                "Usuário do sistema (economia) não encontrado. Configure-o primeiro.",
            )

        deposit_coins = self.pricing_strategy.calcularPrecoDeposito()

        # Sistema repassa moedas para o depositante
        if not self.sistema_economia.repassarMoedas(
            system_user.id, depositor.id, deposit_coins
        ):
            self.db.session.rollback()
            return None, "Falha ao repassar moedas de depósito."

        # Adicionar o livro à sessão (já deve estar, mas garante)
        self.db.session.add(book)
        self.db.session.commit()
        self.notification_subject.notify(
            "coin_received",
            user=depositor,
            amount=deposit_coins,
            source_user=system_user,
        )
        return book, "Livro depositado e moedas concedidas."

    def calcularPenalizacao(self, book: Book, user: User):
        last_rental_record = (
            Rental.query.filter_by(book_id=book.id, rentee_id=user.id)
            .order_by(Rental.dataAluguel.desc())
            .first()
        )

        if not last_rental_record:
            print(
                f"Não há registro de aluguel para o livro {book.titulo} e usuário {user.nome}."
            )
            return book, "Nenhum aluguel encontrado para penalização."

        # Calcula a data esperada de devolução
        expected_return_date = last_rental_record.dataAluguel + datetime.timedelta(
            days=self.config.RENTAL_PERIOD_DAYS
        )

        # Se dataDevolucao já estiver preenchida (aluguel anterior já finalizado)
        if last_rental_record.dataDevolucao:
            actual_return_date = last_rental_record.dataDevolucao
        else:  # Aluguel atual sendo devolvido
            actual_return_date = datetime.datetime.utcnow()

        # Calcula os dias de atraso
        overdue_days = max(0, (actual_return_date - expected_return_date).days)

        if overdue_days > 0:
            penalty_amount = self.pricing_strategy.calcularPenalidade(overdue_days)
            new_penalty = Penalty(
                user_id=user.id,
                book_id=book.id,
                tipo="Atraso",
                valor=penalty_amount,
                multiplicador=1.0,
            )

            if new_penalty.aplicar(user):  # Aplica a penalidade e registra a transação
                self.notification_subject.notify(
                    "penalty_applied",
                    user=user,
                    penalty_amount=penalty_amount,
                    book=book,
                )
            else:
                print(
                    f"Penalidade de {penalty_amount} moedas não pode ser aplicada ao usuário {user.nome} por falta de saldo."
                )
        else:
            print(
                f"Livro '{book.titulo}' devolvido no prazo. Nenhuma penalidade aplicada."
            )

        return book, "Penalização calculada."

    def processarReserva(self, book_id: str, user_id: int):
        book = Book.query.get(book_id)
        user = User.query.get(user_id)

        if not book:
            return None, "Livro não encontrado."
        if not user:
            return None, "Usuário não encontrado."

        try:
            return book.estado.reservar(user, self)
        except ValueError as e:
            self.db.session.rollback()
            return None, str(e)
        except Exception as e:
            self.db.session.rollback()
            return None, f"Erro inesperado ao processar reserva: {str(e)}"

    def _execute_reservation(self, book: Book, user: User):
        """Método interno para completar o processo de reserva após a validação do estado."""
        book.reserved_by_id = user.id
        book.alterarEstado(
            "reservado"
        )  # O objeto de estado pode mudar isso, mas garante que o estado da string reflita
        self.db.session.commit()
        self.notification_subject.notify("book_reserved", book=book, user=user)
        return book, "Livro reservado com sucesso."
