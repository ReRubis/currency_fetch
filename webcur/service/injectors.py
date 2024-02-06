from webcur.service.exhachanger import ExchangeRatesService
from webcur.service.external_api.OKXintegration import OKXIntegration

okx_integration = OKXIntegration()


def okx_integration_injector():
    """
    Returns the OKX integration.
    """
    return okx_integration


def main_service_injector():
    """
    Returns the main service.
    """
    integrations = [
        okx_integration_injector()
    ]
    return ExchangeRatesService(integrations)
