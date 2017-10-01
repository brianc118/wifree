# WiFree

Ever been in a situation where you had no wifi or mobile data? _Oh no! How will I connect with the modern world!_

WiFree is a service (coupled with optional Android/iOS apps) that provides directions to the nearest free WiFi access point via SMS. The app simply retrieves your GPS data and puts it into your default messaging app--you're the one that sends it--that way it's fully transparent.

## Where do I get it?

Unfortunately WiFree currently is not available on eith the Apple App Store or the Google Play. Should there be enough interest, we will definitely be putting them up (none of the members are currently in the Apple Developer Program etc.).

Of course you can always build the apps yourself with Android Studio or XCode.

### Usage

Usage is in the form

```
[travelmode],[latitude],[longitude]
```

where `[travelmode]` is in {'walking', 'driving', 'transit'}.

### Examples

## Built With

* [Twilio](https://github.com/twilio/twilio-python) - For SMS on the server side
* [Google Maps Services](https://github.com/googlemaps/google-maps-services-python) - Google Directions API, Google Distance Matrix API etc. for sorting WiFi spots by travel time and directions.
* [Flask](http://flask.pocoo.org/)
* [Foursquare](https://github.com/mLewisLogic/foursquare) - For finding a list of nearby WiFi spots

## Authors

* Brian Chen
* Yogeshwar Velingker
* Krrish Dholakia
* Edward Liu

## License

This project is licensed under the MIT License - see the [LICENSE.ttxt](LICENSE.txt) file for details

## Acknowledgments

* Googlers at HackMIT for giving us free cloud credits :)
