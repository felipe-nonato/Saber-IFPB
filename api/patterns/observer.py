from abc import ABC, abstractmethod
from typing import List
from api.models.user import User
from api.patterns.factory import (
    EmailFactory,
    SMSFactory,
)  # Para os observadores concretos


class Observer(ABC):
    @abstractmethod
    def update(self, subject, event: str, *args, **kwargs):
        pass


class Subject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, event: str, *args, **kwargs):
        for observer in self._observers:
            observer.update(self, event, *args, **kwargs)


# Observador Concreto conforme diagrama: UsuarioObserver
class UsuarioObserver:  # Não herda de Observer genérico para seguir o diagrama estritamente
    def __init__(self, user: User):
        self.user = user

    def notificar(self, mensagem: str):
        """
        Recebe uma mensagem de notificação direta específica para o usuário.
        Conforme diagrama: + notificar(String)
        """
        print(f"Notificação para {self.user.nome}: {mensagem}")
        # Em uma aplicação real, isso desencadearia uma notificação real (push, email, SMS, etc.)
        # através de uma fábrica de notificação.


# Observadores concretos para `Subject` que usam as fábricas de notificação
class CoinReceivedObserver(Observer):
    def __init__(
        self, notifier_factory: EmailFactory
    ):  # Aceita uma fábrica de notificação
        self.notifier_factory = notifier_factory

    def update(self, subject, event: str, *args, **kwargs):
        if event == "coin_received":
            user = kwargs.get("user")
            amount = kwargs.get("amount")
            source_user = kwargs.get("source_user")
            if user and amount is not None:
                message = (
                    f"Você recebeu {amount} moedas de {source_user.nome}."
                    if source_user
                    else f"Você recebeu {amount} moedas."
                )
                notification = self.notifier_factory.criarNotificacao(
                    user.nome, message
                )
                notification.enviar()


class RentalDueObserver(Observer):
    def __init__(
        self, notifier_factory: EmailFactory
    ):  # Aceita uma fábrica de notificação
        self.notifier_factory = notifier_factory

    def update(self, subject, event: str, *args, **kwargs):
        if event == "book_rented":
            book = kwargs.get("book")
            user = kwargs.get("user")
            due_date = kwargs.get("due_date")
            message = f"Você alugou o livro '{book.titulo}'. Data de devolução: {due_date.strftime('%d/%m/%Y')}"
            notification = self.notifier_factory.criarNotificacao(user.nome, message)
            notification.enviar()
        elif event == "book_returned":
            book = kwargs.get("book")
            user = kwargs.get("user")
            message = f"Você devolveu o livro '{book.titulo}'."
            notification = self.notifier_factory.criarNotificacao(user.nome, message)
            notification.enviar()
        elif event == "book_reserved":
            book = kwargs.get("book")
            user = kwargs.get("user")
            message = f"Você reservou o livro '{book.titulo}'."
            notification = self.notifier_factory.criarNotificacao(user.nome, message)
            notification.enviar()
        elif event == "penalty_applied":
            user = kwargs.get("user")
            penalty_amount = kwargs.get("penalty_amount")
            book = kwargs.get("book")
            message = f"Penalização de {penalty_amount} moedas aplicada pelo atraso na devolução do livro '{book.titulo}'."
            notification = self.notifier_factory.criarNotificacao(user.nome, message)
            notification.enviar()
