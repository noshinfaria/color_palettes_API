# color_palettes_API
It's a project to create a web API to create, manage, and share color palettes using Django Rest Framework

# Requirement.txt file is included: https://github.com/noshinfaria/color_palettes_API/blob/main/requirements.txt


# Operators:
- Registration
- Use django default login view
- Create a Color (Attribute contains "Hexa Decimal Value")
- Create color palette (dominant color takes 1 to 2 color; accent color takes 2 to 4 colors)
  - Users can see public color palettes, Only author can see private and public color palettes
  - Author can update the color palette
  - Revision history will be saved
  - Users can mark public color palettes as their favorite and can delete them from favorite
  - Users can search by color (Must be hexa decimal value)



# Server run:

    - command: python manage.py runserver `127.0.0.1:8000`

## Commands

- python -m pip install -r requirements.txt
- python version: ```3.8.5```
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver


