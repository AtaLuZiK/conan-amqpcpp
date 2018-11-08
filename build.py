import copy
import platform

from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name=False)

    if platform.system() != "Windows":
        extend_settings = []
        for settings in builder.items:
            settings = copy.deepcopy(settings)
            settings.options["amqpcpp:shared"] = True
            extend_settings.append(settings)
        builder.items.extend(extend_settings)

    if platform.system() == "Linux":
        extend_settings = []
        for settings in builder.items:
            settings = copy.deepcopy(settings)
            settings.options["amqpcpp:with_internal_tcp_module"] = True
            extend_settings.append(settings)
        builder.items.extend(extend_settings)

    builder.run()
