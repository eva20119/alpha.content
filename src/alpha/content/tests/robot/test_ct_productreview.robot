# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s alpha.content -t test_productreview.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src alpha.content.testing.ALPHA_CONTENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/alpha/content/tests/robot/test_productreview.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a ProductReview
  Given a logged-in site administrator
    and an add Product form
   When I type 'My ProductReview' into the title field
    and I submit the form
   Then a ProductReview with the title 'My ProductReview' has been created

Scenario: As a site administrator I can view a ProductReview
  Given a logged-in site administrator
    and a ProductReview 'My ProductReview'
   When I go to the ProductReview view
   Then I can see the ProductReview title 'My ProductReview'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Product form
  Go To  ${PLONE_URL}/++add++Product

a ProductReview 'My ProductReview'
  Create content  type=Product  id=my-productreview  title=My ProductReview

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the ProductReview view
  Go To  ${PLONE_URL}/my-productreview
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a ProductReview with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the ProductReview title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
