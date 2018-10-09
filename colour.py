'''
Functions to do with colour definitions, conversions, etc.
'''

'''
Convert a colour definition from rgb to xy plus brightness. See:
    https://github.com/mikz/PhilipsHueSDKiOS/blob/master/ApplicationDesignNotes/RGB%20to%20xy%20Color%20conversion.md
'''
def rgb_to_xyb(hexr, hexg, hexb):
    '''
    Step 0: Convert colour components from hex to decimal
    '''
    red, green, blue = [int(x, 16) for x in [hexr, hexg, hexb]]
    '''
    From the link above, the steps are:

    1. Get the RGB values from your color object and convert them to be between 0 and 1. So the 
    RGB color (255, 0, 100) becomes (1.0, 0.0, 0.39)
    '''
    rgb = [x / 255 for x in [red, green, blue]]

    '''
    2. Apply a gamma correction to the RGB values, which makes the color more vivid and more the 
    like the color displayed on the screen of your device. This gamma correction is also applied 
    to the screen of your computer or phone, thus we need this to create the same color on the 
    light as on screen. This is done by the following formulas:

        float red = (red > 0.04045f) ? pow((red + 0.055f) / (1.0f + 0.055f), 2.4f) : (red / 12.92f);
        float green = (green > 0.04045f) ? pow((green + 0.055f) / (1.0f + 0.055f), 2.4f) : (green / 12.92f);
        float blue = (blue > 0.04045f) ? pow((blue + 0.055f) / (1.0f + 0.055f), 2.4f) : (blue / 12.92f);
    '''
    gc_rgb = [gamma_correct(x) for x in rgb]

    '''
    3. Convert the RGB values to XYZ using the Wide RGB D65 conversion formula The formulas used:

        float X = red * 0.649926f + green * 0.103455f + blue * 0.197109f;
        float Y = red * 0.234327f + green * 0.743075f + blue * 0.022598f;
        float Z = red * 0.0000000f + green * 0.053077f + blue * 1.035763f;
    '''
    from numpy import matmul
    coeff = [[0.649926, 0.103455, 0.197109], [0.234327, 0.743075, 0.022598], [0.0, 0.053077, 1.035763]]
    X, Y, Z = matmul(coeff, gc_rgb)

    '''
    4. Calculate the xy values from the XYZ values

        float x = X / (X + Y + Z); float y = Y / (X + Y + Z);
    '''
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)

    '''
    5. Check if the found xy value is within the color gamut of the light, if not continue with 
    step 6, otherwise step 7 When we sent a value which the light is not capable of, the resulting 
    color might not be optimal. Therefor we try to only sent values which are inside the color 
    gamut of the selected light.
    '''
    hue_color_gamut = [[0.675, 0.322], [0.4091, 0.518], [0.167, 0.04]]
    
    if point_in_triangle([x, y], hue_color_gamut):
        '''
        6. Calculate the closest point on the color gamut triangle and use that as xy value The closest
        value is calculated by making a perpendicular line to one of the lines the triangle consists of
        and when it is then still not inside the triangle, we choose the closest corner point of the 
        triangle.
        '''
        # Note that we don't need to do this because the Hue will do it for us
        pass

    '''
    7. Use the Y value of XYZ as brightness The Y value indicates the brightness of the converted color.
    '''
    return x, y, Y

'''
Gamma correction. Here we assume that `value` is between 0.0 and 1.0
'''
def gamma_correct(value):
    if value > 0.04045:
        return pow((value + 0.055) / (1.055), 2.4)
    else:
        return value / 12.92

''' 
Triangle detection
'''
def point_in_triangle(point, triangle):
    b1 = sign(point, triangle[0], triangle[1]) < 0.0
    b2 = sign(point, triangle[1], triangle[2]) < 0.0
    b3 = sign(point, triangle[2], triangle[0]) < 0.0

    return b1 == b2 and b2 == b3

def sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

