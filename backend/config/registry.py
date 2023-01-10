from typing import AnyStr, Set
import re
from venusian import Scanner
from wired import ServiceRegistry

import domain as domain
import application as application

class LibraryRegistry:

    registry = None
    scanner = None

    @classmethod
    def get_registry(cls) -> ServiceRegistry:
        """
        return registry object if it exists or init/kickstart it
        """
        if cls.registry is None:
            cls.init_registry_and_scan()
        return cls.registry

    @classmethod
    def get_scanner(cls) -> Scanner:
        """
        return scanner object if it exists or init/kickstart it
        """
        if cls.scanner is None:
            cls.init_registry_and_scan()
        return cls.scanner

    @classmethod
    def init_registry_and_scan(cls) -> None:
        """
        init registry and scan
        """

        registry = ServiceRegistry()
        # Point the scanner at a package/module and scan
        # scanner.scan(decorators.decorator_args)
        scanner = Scanner(registry=registry)

        scanner.scan(domain)
        scanner.scan(application)
        
        cls.scanner = scanner
        cls.registry = registry


    @classmethod
    def get_all_registered_label(cls, root_key: AnyStr) -> Set[AnyStr]:
        """
        return all registered labels for operations. We just crawl
        registry and do registry introspection.
        """
        if not root_key:
            raise ValueError("root_key parameter is mandatory")

        result = set()
        registry = cls.get_registry()
        for ele in registry._factories.allRegistrations():
            for registred in ele:
                if (
                    isinstance(registred, str)
                    and re.match(f"^{root_key}.*$", registred) is not None
                ):
                    splited_register = registred.split(root_key)
                    if len(splited_register) > 1:
                        result.add(splited_register[1].strip("."))
        return result

    @classmethod
    def check_all_registered(cls):
        """
        check and print all registered labels for operations. We just crawl
        registry and do registry introspection.
        """
        
        registry = cls.get_registry()
        for sub in registry._factories.allSubscriptions():
            print("Sub", sub)

        for ele in registry._factories.allRegistrations():
            print("Element")
            for registred in ele:
                print("  registered", registred)
                


