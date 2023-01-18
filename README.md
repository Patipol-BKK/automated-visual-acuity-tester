# automated-visual-acuity-tester
 
Code for Automated Visual Acuity Tester intended for running on Raspberry Pi and a Linux-based server

## Testing Standards
Results for testing are available in both Snellen and logMAR values.
### Available Optotypes
Currently the program has 5 available optotypes including:
- HOTV
- Landolt C
- Lea Symbols
- Sloan Letters
- Optician-Sans Numbers

### Importing new optotypes
New optotypes can be imported by converting each symbols into `.svg` and then dragging the folder into `/booth-client/optotypes`. The folder must also include a `config.yml` file with the arcmin height in which the optotype figures should be displayed based on 6/6 vision.
```
# Letter height in arcmin
height: 5
```
