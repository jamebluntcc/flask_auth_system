from app.app import create_app
from flask_script import Manager, Server
from flask_migrate import MigrateCommand


app = create_app()
manager = Manager(app)

manager.add_command('runserver',
                    Server(host='0.0.0.0',
                           port=9000,
                           use_debugger=True))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()