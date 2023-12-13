# Infinite Campus Custom Integration

This is custom Home Assistant Integration for [Infinite Campus](https://www.infinitecampus.com/).  

This integration will create several sensor entities for different objects retrieved from [Infinite Campus](https://www.infinitecampus.com) using the [Infinite Campus Parent API](https://github.com/schwartzpub/ic_parent_api) python module.

The entities that will be created are:

- sensor.infinitecampus_students
- sensor.infinitecampus_courses
- sensor.infinitecampus_assignments
- sensor.infinitecampus_terms

Currently this integration simply returns the raw output from the [Infinite Campus API](https://canvas.instructure.com/doc/api/) for these objects.  There is a basic custom card for viewing [Infinite Campus homework assignments](https://github.com/schwartzpub/homeassistant-cards) as well as a card for [Infinite Campus schedules](https://github.com/schwartzpub/homeassistant-cards).

## Installing

As a pre-requisite please install

1. Python3.x
2. PIP
3. The PIP wheel from here https://github.com/schwartzpub/ic_parent_api

To install this integration, clone the repository into your Home Assistant custom_components directory:

```bash
[core-ssh ~]$ cd config/custom_components/
[core-ssh ~]$ mkdir infinitecampus
[core-ssh ~]$ cd infinitecampus
[core-ssh ~]$ git clone https://github.com/schwartzpub/infinite_campus_hassio.git
```

In Home Assistant, navigate to Settings > Devices & Services and click + Add Integration

Select the Infinite Campus integration.

Enter the following information:

- Base URL (https://'<your_districts_server>'.infinitecampus.com)  substitute the full domain name that shows in your browsers url field to the .com and no more
- District  - at the login page past the search for your district you can inspect the page and find the appName as shown in the screenshot - this is your District
- Username
- Password

![Screenshot 2022-09-16 171957](https://user-images.githubusercontent.com/13734613/190816004-a062b221-0653-4655-9b37-b67211350e6b.jpg)
