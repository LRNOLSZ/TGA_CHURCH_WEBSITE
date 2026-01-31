from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        import api.signals  # Register signals when app is ready
        self.setup_scheduler()
    
    def setup_scheduler(self):
        """Initialize background scheduler for exchange rate updates"""
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.cron import CronTrigger
            from django.core.management import call_command
            import atexit
            
            # Create scheduler
            scheduler = BackgroundScheduler()
            
            # Schedule exchange rate update daily at midnight (00:00)
            scheduler.add_job(
                func=lambda: call_command('update_exchange_rates'),
                trigger=CronTrigger(hour=0, minute=0),
                id='update_exchange_rates',
                name='Update Exchange Rates Daily',
                replace_existing=True,
                misfire_grace_time=15
            )
            
            if not scheduler.running:
                scheduler.start()
                logger.info('✅ Scheduler started - Exchange rates will update daily at midnight (00:00)')
            
            # Shut down the scheduler when Django exits
            atexit.register(lambda: scheduler.shutdown() if scheduler.running else None)
            
        except ImportError:
            logger.warning('⚠️ APScheduler not installed. Exchange rates will need manual updates.')
        except Exception as e:
            logger.error(f'❌ Error starting scheduler: {str(e)}')
