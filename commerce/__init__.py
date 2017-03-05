def get_cart(session):
    '''
    Given a Django session, if the cart exists, return it;
    otherwise return an empty cart.
    '''

    if 'cart' not in session:
        session['cart'] = {}

    return session['cart']
