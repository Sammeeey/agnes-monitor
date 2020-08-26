from spidermon import Monitor, MonitorSuite, monitors
from spidermon.contrib.actions.telegram.notifiers import SendTelegramMessageSpiderFinished


@monitors.name('Item count')
class ItemCountMonitor(Monitor):

    @monitors.name('You may have new exam results!')
    def test_maximum_number_of_items(self):
        item_extracted = getattr(
            self.data.stats, 'item_scraped_count', 0)
        maximum_threshold = 27

        msg = 'Extracted more than {} items'.format(
            maximum_threshold)
        self.assertTrue(
            item_extracted <= maximum_threshold, msg=msg
        )


class SpiderCloseMonitorSuite(MonitorSuite):

    monitors = [
        ItemCountMonitor,
    ]

    monitors_failed_actions = [
        SendTelegramMessageSpiderFinished,
    ]