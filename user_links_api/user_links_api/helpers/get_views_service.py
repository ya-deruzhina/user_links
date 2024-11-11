from glob import glob
from core.loggers import logger


class GetViewsService:
    TARGET_FOLDER = "apps"

    @classmethod
    def _get_views_data(cls, module_name):
        # get paths to views for automatic import
        module_name = module_name.replace("/", ".").replace(".py", "")
        return module_name

    @classmethod
    def call(cls, version):
        # scan all 'urlpatterns' folders in TARGET_FOLDER recursively
        views_modules = []

        files_with_views = glob(
            f'{cls.TARGET_FOLDER}/**/urls_{version}.py', recursive=True)

        for module_path in files_with_views:
            try:
                views_modules.append(cls._get_views_data(module_path))
            except Exception as e:
                logger.info(f"App {module_path} is not checked for views")
                logger.exception(e)

        return views_modules
