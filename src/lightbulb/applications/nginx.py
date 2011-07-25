#!/usr/bin/env python

# LightBulb
# Copyright (c) 2011 Luke Carrier
# Licensing information available at
#   http://github.com/cloudflux/lightbulb

from subprocess import Popen
from tarfile import TarFile

import lightbulb.apphelpers as apphelpers
import lightbulb.exceptions as exceptions
from lightbulb.systemspecific import exec_elevated, which
from lightbulb.systemspecific.packagefilters import pkg_filter
from lightbulb.systemspecific.packagemanagers import pkg_mgr

# Default paths
#   These values are the failsafe defaults we'll use if none were specified.
#   If the default value is None, as is seen for the global install prefix,
#   we'll throw a Big Scary Message and quit -- assuming things like this is
#   simply too dangerous and out of our scope ;)
#
#   All of this magic takes place in ComponentProfile._init_paths(), itself a
#   helper of __init__().
paths = {
    "prefix"    : ("--prefix", None,),
    "conf"      : ("--conf-path", "etc/nginx.conf",),
    "lock"      : ("--lock-path", "var/nginx.lock",),
    "http-log"  : ("--http-log-path", "var/log/access_log",),
    "error-log" : ("--error-log-path", "var/log/error_log",),
    "pid"       : ("--pid-path", "var/nginx.pid",),
    "sbin"      : ("--sbin-path", "sbin/nginx",),
}

# Optional modules information
#   Here, we outline the modules available for the build, with our names (dict
#   keys), their parameters names within the configure script (1st value of the
#   list) and our pseudo identifiers for their dependencies (2nd value).
#
#   Soon, we'll also record version information, though I'm not quite sure how
#   yet (this would need to bear in mind deprecation).
modules = {
    # Eventing modules
    "poll"  : ("--with-poll_module",),
    "rtsig" : ("--with-rtsig_module",),
    "select": ("--without-select_module",),

    # HTTP modules
    "http"                 : ("--without-http",),
    "http-addition"        : ("--with-http_addition_module",),
    "http-auth-basic"      : ("--without-http_auth_basic_module",),
    "http-autoindex"       : ("--without-http_autoindex_module",),
    "http-browser"         : ("--without-http_browser_module",),
    "http-charset"         : ("--without-http_charset_module",),
    "http-dav"             : ("--with-http_dav_module",),
    "http-empty-gif"       : ("--without-http_empty_gif_module",),
    "http-fastcgi"         : ("--without-http_fastcgi_module",),
    "http-flv"             : ("--with-http_flv_module",),
    "http-geo"             : ("--without-http_geo_module",),
    "http-gzip"            : ("--without-http_gzip_module", ["zlib-dev"],),
    "http-limit-zone"      : ("--without-http_limit_zone_module",),
    "http-map"             : ("--without-http_map_module",),
    "http-memcached"       : ("--without-http_memcached_module",),
    "http-perl"            : ("--with-http_perl_module",),
    "http-proxy"           : ("--without-http_proxy_module",),
    "http-realip"          : ("--with-http_realip_module",),
    "http-referer"         : ("--without-http_referer_module",),
    "http-rewrite"         : ("--without-http_rewrite_module", ["pcre-dev"],),
    "http-ssi"             : ("--without-http_ssi_module",),
    "http-ssl"             : ("--with-http_ssl_module", ["ssl-dev"],),
    "http-stub-status"     : ("--with-http_stub_status_module",),
    "http-sub"             : ("--with-http_sub_module",),
    "http-upstream-ip-hash": ("--without-http_upstream_ip_hash_module",),
    "http-userid"          : ("--without-http_userid_module",),

    # Mail options
    "mail"    : ("--with-mail"),
    "mail_ssl": ("--with-mail_ssl_module"),
}

# The %s im this should be replaced with the version number
source_url_format = "http://nginx.org/download/nginx-%s.tar.gz"

versions = (
    "0.5.38",
    "0.6.39",
    "0.7.69",
    "0.8.51",
    "0.8.52",
    "0.8.53",
    "0.8.54",
    "0.8.55",
    "1.0.1",
    "1.0.2",
    "1.0.3",
    "1.0.4",
    "1.0.5",
)

class ComponentBuilder:
    """
    nginx component builder class.

    This class provides the necessary logic to handle compiling the nginx web
    server within LightBulb.
    """

    def __init__(self, component_profile, logger, work_dir):
        """
        """

        global pkg_filter # These are imported above and are initialised in
        global pkg_mgr    # their respective packages

        self._profile    = component_profile
        self._logger     = logger
        self._work_dir   = work_dir
        self._pkg_filter = pkg_filter
        self._pkg_mgr    = pkg_mgr

        self._source_url     = source_url_format %(self._profile.version)
        self._target     = "%s/nginx-%s.tar.gz" %(self._work_dir,
          self._profile.version)
        self._source_dir = "%s/nginx-%s" %(self._work_dir,
          self._profile.version)

        self._install_dependencies()
        self._download()
        self._extract()
        self._configure()
        self._build()
        self._install()

    def _install_dependencies(self):
        """
        """

        self._logger.info("Installing nginx build dependencies")

        deps = []
        for dep in self._profile.dependencies:
            deps.append(self._pkg_filter[dep])

        self._pkg_mgr.install_pkgs(deps)

        self._logger.info("Finished installing nginx build dependencies")

    def _download(self):
        """
        @todo verification though MD5, SHA1 or PGP sums
        """

        self._logger.info("Downloading nginx source code")

        with open(self._target, "wb") as t:
            apphelpers.Download.download(self._source_url, t)

        # Since our download dotter method doesn't output a new line on its
        # final run (it can't, it has no way of knowing it's being called for
        # the final time), we fix shell output with this print call
        print("")

        self._logger.info("Finished downloading nginx source code")

    def _extract(self):
        """
        """

        self._logger.info("Extracting nginx source code")

        source = TarFile.open(self._target, "r|gz")
        source.extractall(self._work_dir)

        self._logger.info("Finished extracting nginx source code")

    def _configure(self):
        """
        """

        self._logger.info("Configuring nginx for compilation")

        configure_opts = ["./configure"]

        # Make sure we get those paths
        for (key, value) in paths.items():
            configure_opts.append("%s=%s" %(
              paths[key][0], self._profile.paths[key]))

        # Disable all modules by default
        for module in modules.items():
            if module[1][0].startswith("--without"):
                configure_opts.append(module[1][0])

        # Enable all user-specified modules
        for module in self._profile.modules:
            if modules[module][0].startswith("--without"):
                configure_opts.remove(modules[module][0])
            else:
                configure_opts.append(modules[module][0])

        configure_line = " ".join(configure_opts)

        self._logger.info("Using configure line:\n%s" %(configure_line))

        proc = Popen(configure_opts, bufsize = -1, stdin = None,
          cwd = self._source_dir)
        if proc.wait() > 0:
            raise exceptions.ApplicationBuildError("Configure failed")

        self._logger.info("Finished configuring nginx for compilation")

    def _build(self):
        """
        """

        self._logger.info("Compiling nginx source code")

        proc = Popen(["make"], bufsize = -1, stdin = None,
          cwd = self._source_dir)
        if proc.wait() > 0:
            raise exceptions.ApplicationBuildError("Compilation failed")

        self._logger.info("Finished compiling nginx source code")

    def _install(self):
        """
        """

        self._logger.info("Installing nginx")

        proc = exec_elevated([which("make"), "install"], cwd = self._source_dir)
        if proc.wait() > 0:
            raise exceptions.ApplicationBuildError("Installation failed")

        self._logger.info("Finished installing nginx")

class ComponentProfile:
    """
    nginx component profile.

    This class provides an abstraction over the various configuration options
    which can be specified at configure- and compile-time.
    """

    # The values we export
    application  = "nginx"
    version      = ""
    paths        = {}
    auth_cred    = {}
    modules      = []
    dependencies = []

    def __init__(self, dict):
        """
        Initialise the component profile.

        This method initialises the class as a data structure for the nginx
        configuration options. Here, we call a ton of helper methods which set
        the values of the application version we're building, the various
        different utility paths, the system user and group the daemon should be
        configured to execute under and any modules that should be compiled in
        to the server binary.
        """

        self.raw = dict
        self._init_version()
        self._init_paths()
        self._init_modules()
        self._init_dependencies()

    def __str__(self):
        """
        Return a string representation.
        """

        paths = "\n".join("%s: %s" %(key, value) for (key, value)
          in self.paths.items())
        modules = "\n".join("* %s" %(value) for value in self.modules)
        dependencies = "\n".join("* %s" %(value) for value in self.dependencies)

        return "Application: %s\n\nPaths:\n%s\n\nModules:\n%s\n\nDependencies:\n%s" %(
          self.raw["application"], paths, modules, dependencies)

    def _init_version(self):
        """
        Initialise version information.

        This is a helper method for __init__().

        Get the version number from the profile file and ensure we're actually
        able to build this version. If it's not within our versions dictionary,
        we'll raise an error and bail out early.
        """

        if self.raw["version"] not in versions:
            raise exceptions.UnsupportedApplicationVersionError(
              self.raw["application"], self.raw["version"])

        self.version = self.raw["version"]

    def _init_paths(self):
        """
        Initialise filesystem path information.

        This is a helper method for __init__().

        Grab the paths specified in the profile and store them.
        """

        for (key, value) in paths.items():
            try:
                raw = self.raw["paths"][key]
            except KeyError:
                raw = paths[key][1]

            if not raw.startswith("/"):
                if key == "prefix":
                    raise exceptions.InvalidApplicationPath(
                      self.raw["application"], key, value)

                raw = "%s/%s" %(self.raw["paths"]["prefix"], raw)

            self.paths[key] = raw

    def _init_modules(self):
        """
        Initialise module list.

        This is a helper method for __init__().

        The nginx daemon doesn't support the concept of dynamic module loading
        for reasons pertaining to performance, though it does support statically
        compiling modules into the binary. Here, we initialise a list of
        module-related configuration options to pass to the ./configure script.
        """

        for module in self.raw["modules"]:
            self.modules.append(module)

    def _init_dependencies(self):
        """
        Initialise dependencies.

        This is a helper method for __init__().
        """

        self.dependencies.extend(["gcc", "make"])

        for module in self.modules:
            try:
                self.dependencies.extend(modules[module][1])
            except IndexError:
                pass

