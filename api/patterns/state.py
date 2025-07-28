from abc import ABC, abstractmethod
import datetime

# Não importa diretamente o DB aqui, pois os objetos de estado operam no livro
# e delegam a lógica complexa (como operações de DB, notificações) ao mediador.


class EstadoLivro(ABC):
    def __init__(self, book):
        self._book = book

    @abstractmethod
    def alugar(self, user, mediator):
        pass

    @abstractmethod
    def devolver(self, user, mediator):
        pass

    @abstractmethod
    def reservar(self, user, mediator):
        pass


class Disponivel(EstadoLivro):
    def alugar(self, user, mediator):
        if self._book.reserved_by_id and self._book.reserved_by_id != user.id:
            raise ValueError(
                f"Livro '{self._book.titulo}' está reservado para outro usuário."
            )

        # Delega ao mediador para a lógica complexa de aluguel
        # O mediador precisa chamar de volta um método interno após a validação
        result_book, message = mediator._execute_rental(self._book, user)
        if result_book:
            self._book.set_estado(Alugado(self._book))  # Transiciona o estado do livro
        return result_book, message

    def devolver(self, user, mediator):
        raise ValueError(
            f"Livro '{self._book.titulo}' já está disponível. Não pode ser devolvido."
        )

    def reservar(self, user, mediator):
        if self._book.reserved_by_id:
            raise ValueError(f"Livro '{self._book.titulo}' já está reservado.")

        # Delega ao mediador para a lógica de reserva
        result_book, message = mediator._execute_reservation(self._book, user)
        if result_book:
            self._book.set_estado(
                Reservado(self._book)
            )  # Transiciona o estado do livro
        return result_book, message


class Alugado(EstadoLivro):
    def alugar(self, user, mediator):
        raise ValueError(
            f"Livro '{self._book.titulo}' já está alugado por {self._book.rentee.nome if self._book.rentee else 'alguém'}."
        )

    def devolver(self, user, mediator):
        if self._book.rentee_id != user.id:
            raise ValueError(f"Livro '{self._book.titulo}' não está alugado por você.")

        # Delega ao mediador para a lógica complexa de devolução
        result_book, message = mediator._execute_return(self._book, user)
        if result_book:
            # O estado pode se tornar 'disponivel' ou 'reservado' após a devolução.
            # O mediador lida com isso e altera o `_estado_nome` do livro diretamente.
            # Não é necessário um set_estado explícito aqui, pois o mediador já define.
            pass
        return result_book, message

    def reservar(self, user, mediator):
        if self._book.rentee_id == user.id:
            raise ValueError(f"Você já alugou o livro '{self._book.titulo}'.")
        if self._book.reserved_by_id:
            raise ValueError(f"Livro '{self._book.titulo}' já está reservado.")

        # Permite a reserva de um livro já alugado (para ser o próximo a alugar)
        result_book, message = mediator._execute_reservation(self._book, user)
        if result_book:
            # O estado do livro continua "Alugado", mas agora ele tem uma reserva.
            # O `_estado_nome` do livro não muda para 'reservado' até que seja devolvido e a reserva seja ativada.
            pass
        return result_book, message


class Reservado(EstadoLivro):
    def alugar(self, user, mediator):
        if self._book.reserved_by_id != user.id:
            raise ValueError(
                f"Livro '{self._book.titulo}' está reservado para outro usuário. Não pode ser alugado por você."
            )

        # Apenas o usuário reservado pode alugá-lo
        # Após o aluguel, a reserva é limpa e o estado muda para Alugado
        self._book.reserved_by_id = None  # Limpa a reserva uma vez alugado
        result_book, message = mediator._execute_rental(self._book, user)
        if result_book:
            self._book.set_estado(Alugado(self._book))  # Transiciona o estado do livro
        return result_book, message

    def devolver(self, user, mediator):
        raise ValueError(
            f"Livro '{self._book.titulo}' está reservado. Não pode ser devolvido neste estado diretamente."
        )

    def reservar(self, user, mediator):
        if self._book.reserved_by_id == user.id:
            raise ValueError(f"Livro '{self._book.titulo}' já está reservado por você.")
        else:
            raise ValueError(
                f"Livro '{self._book.titulo}' já está reservado por outro usuário."
            )
