from abc import ABC, abstractmethod
from api.config import Configuration


class PrecificacaoStrategy(ABC):
    def __init__(self, config):
        self.config = config  # Assume que config é injetado no construtor

    def calcularPrecoDeposito(self):
        if hasattr(self.config, "DEPOSIT_COINS"):
            return self.config.DEPOSIT_COINS
        else:
            raise ValueError(
                "Configuração 'DEPOSIT_COINS' não encontrada. Verifique o arquivo de configuração."
            )

    @abstractmethod
    def calcularPrecoAluguel(self, rental_duration_days: int) -> float:
        pass

    @abstractmethod
    def calcularPrecoDeposito(self) -> float:
        pass

    @abstractmethod
    def calcularPenalidade(self, overdue_days: int) -> float:
        pass

    @abstractmethod
    def aplicarDesconto(self, price: float) -> float:
        pass

    @abstractmethod
    def aplicarBonus(self, price: float) -> float:
        pass


class PorRecorrencia(PrecificacaoStrategy):
    # Esta estratégia poderia, por exemplo, dar descontos para locatários frequentes,
    # ou bônus para depositantes frequentes.
    def calcularPrecoAluguel(self, rental_duration_days: int) -> float:
        base_price = rental_duration_days * self.config.RENT_COINS_PER_DAY
        # Exemplo: desconto por recorrência (simplificado)
        return self.aplicarDesconto(base_price)

    def calcularPrecoDeposito(self) -> float:
        base_deposit = self.config.DEPOSIT_COINS
        # Exemplo: bônus por recorrência (simplificado)
        return self.aplicarBonus(base_deposit)

    def calcularPenalidade(self, overdue_days: int) -> float:
        return overdue_days * self.config.PENALTY_COINS_PER_DAY

    def aplicarDesconto(self, price: float) -> float:
        # Exemplo: 10% de desconto para "usuários recorrentes" (a lógica real verificaria o histórico do usuário)
        print("Aplicando 10% de desconto por recorrência.")
        return price * 0.9

    def aplicarBonus(self, price: float) -> float:
        # Exemplo: 5 moedas extras para "depositantes recorrentes"
        print("Aplicando 5 moedas de bônus por recorrência.")
        return price + 5


class PorTempo(PrecificacaoStrategy):
    # Esta estratégia simplesmente calcula com base no tempo, sem lógica de recorrência.
    def calcularPrecoAluguel(self, rental_duration_days: int) -> float:
        return rental_duration_days * self.config.RENT_COINS_PER_DAY

    def calcularPrecoDeposito(self) -> float:
        return self.config.DEPOSIT_COINS

    def calcularPenalidade(self, overdue_days: int) -> float:
        return overdue_days * self.config.PENALTY_COINS_PER_DAY

    def aplicarDesconto(self, price: float) -> float:
        return price  # Sem desconto baseado apenas no tempo

    def aplicarBonus(self, price: float) -> float:
        return price  # Sem bônus baseado apenas no tempo

    def getTipo(self) -> str:  # Conforme diagrama
        return "Precificação Por Tempo"
