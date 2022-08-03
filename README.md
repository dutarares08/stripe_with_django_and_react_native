# stripe_with_django_and_react_native
DJANGO FILE IS THERE IS CALLED views.py

    """
        Use this model to store additional information about the user.
        This model is not used for authentication or authorization.
        Use to store data like premium status, notifications token, etc

        You can retrive directly from stripe based on stripe_customer_id
        -> https://stripe.com/docs/api/cards/delete

        ending card, list of all cards which is default, change default one 
        -> https://stripe.com/docs/api/customers/update

        Much better to how to upgrade or downgrade subscription:
        -> https://stripe.com/docs/billing/subscriptions/upgrade-downgrade
        (also in this page you can see billingcycle = CAND SA IA BANII, azi, acum maine)
    """
    
