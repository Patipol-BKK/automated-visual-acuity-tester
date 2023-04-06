# automated-visual-acuity-tester
 
This is the code for Automated Visual Acuity Tester intended for running on Raspberry Pi and a Linux-based server. The test is based on testing the examinee's ability to see the optotypes shown on a display by listening the responses through voice commands. Mainly, the Raspberry Pi is responsible for rendering optotypes on the testing display and recording voice signals to be sent to the server for transcription.

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
New optotypes can be imported by converting each symbols into `.svg` and then dragging the folder into [/booth-client/components/optotypes](/booth-client/components/optotypes). The folder must also include a `config.yml` file with the arcmin height in which the optotype figures should be displayed based on 6/6 vision.
```yaml
# Letter height in arcmin
height: 5
```
TODO
- Generate new voice sample from extracting voice clips you e.g. youtube then training a model based on that to produce new alphabetical readings
