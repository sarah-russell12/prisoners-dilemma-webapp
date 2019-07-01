from django.test import TestCase

# Create your tests here.
class HomeViewTests(TestCase):
    def test_home_without_user_logged_in(self):
        """
        A home page without a user logged in will show a 'login or signup'
        set of links in the header.
        """
        return
        
        
    def test_home_with_user_logged_in(self):
        """
        A home page with a user logged in will show a 'Hi, username. Logout'
        set of links in the header.
        """
        return
    
class AccountViewTests(TestCase):
    def test_account_without_user_logged_in(self):
        """
        An account page without a user logged in will show 'You are not logged
        in." in the response.
        An account page without a user logged in will show a 'login or signup'
        set of links in the header.
        """
        return
    
    def test_account_with_user_logged_in(self):
        """
        An account page with a user logged in will show the account information
        of the user in the response.
        An account page with a user logged in will show a 'Hi, username. Logout'
        set of links in the header.
        """
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