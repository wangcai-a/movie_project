from app import app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


def make_shell_context():
    """ make_shell_context() 注册了程序, 数据库实例, 以及模型."""
    return dict(app=app, db=db)


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()