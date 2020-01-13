
import sys,os




if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AccessGateway.settings")
    import django
    django.setup()


    from  backend import main
    interactive_obj = main.ArgvHandler(sys.argv)
    # interactive_obj.call()
    interactive_obj.run()