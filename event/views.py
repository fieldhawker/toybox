from django.shortcuts import render

# Create your views here.
import logging

from django.http import HttpResponse
from services import scraping_service

logger = logging.getLogger('normal')

def index(request):

    logger.debug('-- START --')

    schedules = scraping_service.ScrapingService.get_blueimpulse_schedule()
    logger.debug(schedules)

    logger.debug('-- END --')

    return render(request, 'event/index.html', {
        'hoge': 'test string',
        'fuga': '<br>tag</br>',
        'schedules': schedules,
    })
