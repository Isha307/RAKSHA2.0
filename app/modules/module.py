# modules ka backend with firebase

# resume from prev session, purane variables fetch krke
# flag variable - that will store where user last left

from flask import session

flag = 1


# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Define the blueprint: 'auth', set its url prefix: app.url/auth
modules = Blueprint('auth', __name__ )

# Set the route and accepted methods
@modules.route('/one', methods=['GET', 'POST'])
def one():

    return render_template(f"modules/module{flag}.html")

# Set the route and accepted methods
@modules.route('/two', methods=['GET', 'POST'])
def two():
    
    #get flag from firebase -> user.flag
    return render_template(f"modules/module{flag}.html")

# Set the route and accepted methods
@modules.route('/three', methods=['GET', 'POST'])
def three():
    
    return render_template(f"modules/module{flag}.html")