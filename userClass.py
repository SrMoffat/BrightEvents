# The model that handles the users of the application
import re


class UserManager(object):

    def __init__(self):
        """The initialization of the user_class with an empty user_list list"""
        self.user_list = []

    def registerUser(self, username, email, password, cpassword):
        # Creating registered users that have signed up by adding to dictionary
        # Empty dict to hold each user
        user_dict = {}
        # Check for existing user
        for user in self.user_list:
            if username == user['username']:
                # flash ("The username already exists, please log in!")
                return "existing_user"
        # Check for right password length
        if len(password) < 6:
            # flash("Your password should be at least 6 characters long")
            return "invalid_password"
        # Check for special characters in username
        elif not re.match("^[a-zA-Z0-9_]*$", username):
            # flash ("No special characters (. , ! space [] )")
            return "invalid_charcaters"
        # Check for correct email
        elif not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", email):
            # flash ("Please provide a valid email address")
            return "invalid_email"
        # Password Mismatch
        elif password == cpassword:
            user_dict['username'] = username
            user_dict['email'] = email
            user_dict['password'] = password
            self.user_list.append(user_dict)
        else:
            return "password_mismatch"  # flash ("The passwords do not match!")
        # flash("You have been successfully registered. You can now login!")
        return "success"

    def signin(self, username, password):
        for user in self.user_list:
            if username == user['username']:
                if password == user['password']:
                    return 'successful_login'
                return 'password_mismatch'
            return 'unregistered_user'
        return render_template('signin.html')
