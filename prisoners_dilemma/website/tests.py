from django.test import TestCase
from django.urls import reverse

from .models import PlayerUser

# Utitlity functions
def createPlayer(username, password):
    """
    Creates a player who has not played the game before
    """
    user = PlayerUser.objects.create_user(username=username)
    user.set_password(password)
    user.save()
    return

def createExperiencedPlayer(username, password, points=10, games=1, coop_actions=8):
    """
    By default creates a user that has played 1 game and earned 10 points by
    not cooperating when their opponent cooperated twice, and cooperated the
    other 8 times when their opponent did not.
    """
    user = PlayerUser.objects.create_user(username=username)
    user.set_password(password)
    user.points = points
    user.games_completed = games
    user.cooperative_actions = coop_actions
    user.save()
    user.updateCooperativeScore()
    user.save()
    return

# Create your tests here.
class HomeViewTests(TestCase):
    def getClientResponse(self):
        return self.client.get(reverse('home'))
    
    def test_home_without_user_logged_in(self):
        """
        A home page without a user logged in will show a 'login or signup'
        set of links in the header.
        """
        response = self.getClientResponse()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Sign Up")
        
        
    def test_home_with_user_logged_in(self):
        """
        A home page with a user logged in will show a 'Hi, username. Logout'
        set of links in the header.
        """
        createPlayer("usr1", "PssWrd123")
        self.client.login(username="usr1", password="PssWrd123")
        response = self.getClientResponse()
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "usr1")
        self.assertContains(response, "Logout")
        return
    
class ProfileViewTests(TestCase):
    def getClientResponse(self):
        return self.client.get(reverse('profile'))
    
    def test_profile_without_user_logged_in(self):
        """
        An profile page without a user logged in will show 'You are not logged
        in." in the response.
        An account page without a user logged in will show a 'login or signup'
        set of links in the header.
        """
        response = self.getClientResponse()
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are not logged in.")
        self.assertContains(response, "Login")
        self.assertContains(response, "Sign Up")
        return
    
    def test_account_with_user_logged_in(self):
        """
        An profile page with a user logged in will show the account information
        of the user in the response, like the number of points earned.
        An account page with a user logged in will show a 'Hi, username. Logout'
        set of links in the header.
        """
        createPlayer("usr1", "PssWrd123")
        self.client.login(username="usr1", password="PssWrd123")
        response = self.getClientResponse()
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "usr1")
        self.assertContains(response, "Logout")
        self.assertContains(response, "Points: 0")
        self.assertContains(response, "Games completed: 0")
        return
    
    def test_account_when_user_has_points(self):
        """
        A profile page of a player who has played the game will show stats
        reflecting that
        """
        createExperiencedPlayer("user1", "PssWrd123")
        self.client.login(username="user1", password="PssWrd123")
        response = self.getClientResponse()
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "user1")
        self.assertContains(response, "Logout")
        self.assertContains(response, "Points: 10")
        self.assertContains(response, "Games completed: 1")
        self.assertContains(response, "Cooperative Score: 0.8")
        return

class LoginViewTests(TestCase):
    def getClientResponse(self):
        return self.client.get(reverse('login'))
    
    def test_login_without_user_logged_in(self):
        """
        A login page without a user logged in will display the form
        """
        response = self.getClientResponse()
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Sign Up")
        self.assertContains(response, "Username")
        self.assertContains(response, "Password")
        return
        
    def test_login_with_user_logged_in(self):
        """
        A login page with a user logged in will inform them that they are
        already logged in
        """
        createPlayer("usr", "PssWrd123")
        self.client.login(username="usr", passowrd="PssWrd123")
        response = self.getClientResponse()
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "usr")
        self.assertContains(response, "Logout")
        self.assertContains(response, "You are already logged in")
        self.assertContains(response, "Return to the Home page")
        return
    
class SignupViewTests(TestCase):
    def getClientResponse(self):
        return self.client.get(reverse('signup'))
    
    def test_signup_without_user_logged_in(self):
        """
        A sign up page without a user logged in will display the form
        """
        response = self.getClientResponse()
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Sign Up")
        self.assertContains(response, "Username")
        self.assertContains(response, "Password")
        self.assertContains(response, "password must contain")
        return
        
    def test_signup_with_user_logged_in(self):
        """
        A sign up page with a user logged in will inform them that they already
        have an account
        """
        createPlayer("usr", "PssWrd123")
        self.client.login(username="usr", password="PssWrd123")
        response = self.getClientResponse()
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "usr")
        self.assertContains(response, "Logout")
        self.assertContains(response, "You already have an account")
        return
        
class ChangePasswordViewTests(TestCase):
    def getClientResponse(self):
        return self.client.get(reverse('password_change'))
    
    def test_change_password_without_user_logged_in(self):
        """
        A change password page with a user that is not logged in will inform
        them they are not logged in and will offer a link to the forgot
        password page
        """
        response = self.getClientResponse()
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Sign Up")
        self.assertContains(response, "You are not logged in")
        self.assertContains(response, "Did you forget your password?")
        return

    def test_change_password_with_user_logged_in(self):
        """
        A change password page with a user that is logged in will display the
        form
        """ 
        createPlayer("usr", "PssWrd123")
        self.client.login(username="usr", password="PssWrd123")
        response = self.getClientResponse()
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "usr")
        self.assertContains(response, "Logout")
        self.assertContains(response, "New password")
        self.assertContains(response, "Confirm password")
        return
    
class LeaderboardViewTests(TestCase):
    def test_leaderboard_without_user_logged_in(self):
        """
        A leaderboard page without a user logged in will show a 'login' link
        and a 'sign up' link in the header.
        """
        return
    
    def test_leaderboard_with_user_logged_in(self):
        """
        A leaderboard page with a user logged in will show a 
        'Hi, username. Logout' set of links in the header.
        """
        return
    
    def test_leaderboard_with_no_users(self):
        """
        A leaderboard page with no users will give a "There is no leaderboard"
        message in the response.
        """
        return
        
    def test_leaderboard_with_one_user_no_points(self):
        """
        A leaderboard page with one user that has no points will give a
        "There is no leaderboard" message in the response
        """
        return
    
    def test_leaderboard_with_one_user_with_points(self):
        """
        A leaderboard page with one user that has points will show a table
        with the user listed
        """
        return
    
    def test_leaderboard_with_multiple_users(self):
        """
        A leaderboard page with multiple users with points will show a table
        with the users listed by decending order of points.
        The leaderboard page will not display users with no points.
        """
        return
    
    def test_leaderboard_with_multiple_users_same_score(self):
        """
        A leaderboard page with multiple users with points will show a table
        with the users listed by decending order of points.
        Users that have the same number of points will be given the same rank
        number, and the next player after them given the usual rank number as
        their order in the rankings.  A tie for rank 2 should look like this:
            Rank    User        Points
            1       usr_1       46
            2       user_2      30
            2       user_3      30
            4       user_4      1
        """
        return