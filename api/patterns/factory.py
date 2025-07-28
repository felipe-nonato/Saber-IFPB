from abc import ABC, abstractmethod


# --- Produtos de Notificação ---
class Notification(ABC):
    def __init__(self, destinatario: str, mensagem: str):
        self._destinatario = destinatario
        self._mensagem = mensagem

    @abstractmethod
    def enviar(self):
        pass

    def getDestinatario(self) -> str:
        return self._destinatario

    def formatarMensagem(self) -> str:
        return self._mensagem


class EmailNotification(Notification):
    def enviar(self):
        print(f"Enviando Email para {self._destinatario}: {self._mensagem}")
        # Placeholder para a lógica real de envio de email


class SMSNotification(Notification):
    def enviar(self):
        print(f"Enviando SMS para {self._destinatario}: {self._mensagem}")
        # Placeholder para a lógica real de envio de SMS


# --- Fábrica Abstrata ---
class NotificationFactory(ABC):
    @abstractmethod
    def criarNotificacao(self, destinatario: str, mensagem: str) -> Notification:
        pass


# --- Fábricas Concretas ---
class EmailFactory(NotificationFactory):
    def criarNotificacao(self, destinatario: str, mensagem: str) -> Notification:
        return EmailNotification(destinatario, mensagem)

    def criarEmail(self, destinatario: str, mensagem: str) -> EmailNotification:
        # Método específico conforme diagrama
        return self.criarNotificacao(destinatario, mensagem)

    def enviar(self, destinatario: str, mensagem: str):
        # Método específico conforme diagrama, envia diretamente
        notification = self.criarNotificacao(destinatario, mensagem)
        notification.enviar()


class SMSFactory(NotificationFactory):
    def criarNotificacao(self, destinatario: str, mensagem: str) -> Notification:
        return SMSNotification(destinatario, mensagem)

    def criarSMS(self, destinatario: str, mensagem: str) -> SMSNotification:
        # Método específico conforme diagrama
        return self.criarNotificacao(destinatario, mensagem)

    def enviar(self, destinatario: str, mensagem: str):
        # Método específico conforme diagrama, envia diretamente
        notification = self.criarNotificacao(destinatario, mensagem)
        notification.enviar()
