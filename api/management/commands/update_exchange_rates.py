import requests
from django.core.management.base import BaseCommand
from api.models import ExchangeRate


class Command(BaseCommand):
    help = 'Fetch and update exchange rates from exchangerate-api.com (free tier, no API key needed)'

    def handle(self, *args, **options):
        """Fetch exchange rates from free API"""
        try:
            # Using free tier of exchangerate-api.com (no authentication required)
            # Free tier: https://api.exchangerate-api.com/v4/latest/{currency}
            response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=10)
            response.raise_for_status()
            
            data = response.json()
            rates = data.get('rates', {})
            
            if not rates:
                self.stdout.write(self.style.ERROR('No rates received from API'))
                return
            
            # Define common currencies with their names
            currency_names = {
                'USD': 'US Dollar',
                'GHS': 'Ghana Cedi',
                'CUP': 'Cuban Peso',
                'EUR': 'Euro',
                'GBP': 'British Pound',
                'JPY': 'Japanese Yen',
                'INR': 'Indian Rupee',
                'AUD': 'Australian Dollar',
                'CAD': 'Canadian Dollar',
                'CHF': 'Swiss Franc',
                'CNY': 'Chinese Yuan',
                'SEK': 'Swedish Krona',
                'NZD': 'New Zealand Dollar',
                'ZAR': 'South African Rand',
                'BRL': 'Brazilian Real',
                'MXN': 'Mexican Peso',
                'SGD': 'Singapore Dollar',
                'HKD': 'Hong Kong Dollar',
                'NOK': 'Norwegian Krone',
                'KRW': 'South Korean Won',
                'TRY': 'Turkish Lira',
                'RUB': 'Russian Ruble',
                'INR': 'Indian Rupee',
                'AED': 'UAE Dirham',
                'KES': 'Kenyan Shilling',
                'NGN': 'Nigerian Naira',
            }
            
            updated = 0
            created = 0
            
            for currency_code, rate in rates.items():
                currency_name = currency_names.get(currency_code, f'{currency_code} Currency')
                
                exchange_rate, created_flag = ExchangeRate.objects.update_or_create(
                    currency_code=currency_code,
                    defaults={
                        'rate': rate,
                        'currency_name': currency_name
                    }
                )
                
                if created_flag:
                    created += 1
                else:
                    updated += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Exchange rates updated successfully!\n'
                    f'   Created: {created} new rates\n'
                    f'   Updated: {updated} existing rates'
                )
            )
            
        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error fetching exchange rates: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Unexpected error: {str(e)}')
            )
