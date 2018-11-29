import click
from mybrog.extensions import db
from mybrog.models import Admin, Category





def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generates the fake categories, posts, and comments."""
        from mybrog.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts()
        click.echo('Generating %d links...' % 10)
        fake_links()
        click.echo('Generating %d comment...' % comment)
        fake_comments()

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username usedto login')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
            click.echo('Initializing the database...')
            db.create_all()

            admin = Admin.query.first()
            if admin is not None:
                click.echo('The administrator already exists, updating...')
                admin.username = username
                admin.set_password(password)
            else:
                click.echo('Creating the temporary administrator account...')
                admin = Admin(
                    username=username,
                    blog_title='Bluelog',
                    blog_sub_title="No, I'm the real thing.",
                    name='Admin',
                    about='Anything about you.'
                )
                admin.set_password(password)
                db.session.add(admin)

            category = Category.query.first()
            if category is None:
                click.echo('Creating the default category...')
                category = Category(name='Default')
                db.session.add(category)

            db.session.commit()
            click.echo('Done.')

