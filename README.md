# Infinite Campus Custom Integration
This is custom Home Assistant Integration for [Infinite Campus](https://www.infinitecampus.com/) from Instructure.  

This integration will create several sensor entities for different objects retrieved from [Infinite Campus](https://www.infinitecampus.com) using the [Infinite Campus Parent API](https://github.com/schwartzpub/ic_parent_api) python module.

The entities that will be created are:
 - sensor.infinitecampus_students
 - sensor.infinitecampus_courses
 - sensor.infinitecampus_assignments
 - sensor.infinitecampus_terms

Currently this integration simply returns the raw output from the [Infinite Campus API]() for these objects.  There is a basic custom card for viewing [Infinite Campus homework assignments](https://github.com/schwartzpub/homeassistant-cards) as well as a card for [Infinite Campus schedules](https://github.com/schwartzpub/homeassistant-cards).

## Installing
To install this integration, clone the repository into your Home Assistant custom_components directory:

```bash
[core-ssh ~]$ cd config/custom_components/
[core-ssh ~]$ mkdir infinitecampus
[core-ssh ~]$ cd canvas
[core-ssh ~]$ git clone git@github.com:schwartzpub/infinite_campus_hassio .
```

In Home Assistant, navigate to Settings > Devices & Services and click + Add Integration

Select the Canvas integration.

Enter the following information:
 - Base URL (https://<yourdistrict>.infinitecampus.com)
 - District 
 - Username
 - Password
