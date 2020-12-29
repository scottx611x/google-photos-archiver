class TestMediaItemRecorder:
    def test_add_and_lookup(self, test_media_item_recorder, test_photo_media_item):
        assert test_media_item_recorder.lookup(test_photo_media_item) is False
        test_media_item_recorder.add(test_photo_media_item)
        assert test_media_item_recorder.lookup(test_photo_media_item) is True
