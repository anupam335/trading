def test_downloader_import():
    from python.downloader.downloader import Downloader

    assert hasattr(Downloader, "fetch")
