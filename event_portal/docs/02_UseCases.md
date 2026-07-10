# Event Registration Portal

## Use Case 1: User Registers for an Event
### Actor: Attendee
#### Precondition:
The attendee must have access to a web browser and the event registration portal.
#### Main Steps:
1. The attendee opens their web browser and navigates to the event registration portal.
2. They enter their personal information such as name, email, and contact number.
3. They select the event they are interested in from the list of available events.
4. They confirm the details of their registration including number of tickets and payment method.
5. They proceed with the payment using a secure online payment gateway.
6. Upon successful payment, they receive a confirmation message.
#### Postcondition:
The attendee is registered for the selected event and will receive an email confirmation with all necessary details.
#### Alternative Flows:
- **Payment Failure**: If the payment process fails, the system displays an error message, prompting the user to try again or contact customer support.

## Use Case 2: Admin Approves a Registration
### Actor: Event Organizer/Admin
#### Precondition:
The event organizer must have access to the admin interface of the registration portal and be logged in.
#### Main Steps:
1. The organizer logs into the admin interface using their credentials.
2. They navigate to the registrations section where pending or incomplete registrations are listed.
3. They select a specific registration for approval.
4. If necessary, they review additional details such as payment status, personal information, etc.
5. Once verified, they approve the registration by clicking on an "Approve" button.
6. The system sends a confirmation email to the attendee with the registration details.
#### Postcondition:
The registration is approved, and the attendee receives notification of their acceptance.
#### Alternative Flows:
- **Pending Payment**: If the payment has not been received, the organizer may choose to contact the attendee or mark the registration as pending payment.

## Use Case 3: Admin Cancels a Registration
### Actor: Event Organizer/Admin
#### Precondition:
The event organizer must have access to the admin interface of the registration portal and be logged in.
#### Main Steps:
1. The organizer logs into the admin interface using their credentials.
2. They navigate to the registrations section where registered attendees are listed.
3. They select a specific registration for cancellation.
4. They confirm the cancellation with an appropriate message or reason.
5. The system updates the attendee's status as "Cancelled" and sends them a notification of cancellation via email.
6. Any associated fees or deposits are processed according to the portal’s policy.
#### Postcondition:
The registration is cancelled, and the attendee receives confirmation of the cancellation.
#### Alternative Flows:
- **Refund Processing**: If a refund is applicable, it should be initiated and sent to the attendee's payment method.

## Use Case 4: Attendee Updates Registration Details
### Actor: Attendee
#### Precondition:
The attendee must have registered for an event and be logged into their account.
#### Main Steps:
1. The attendee logs into their account on the registration portal.
2. They navigate to their profile section where they can update details such as name, email, or contact number.
3. They make necessary changes and save them by clicking on the "Update" button.
4. The system confirms that the details have been updated successfully.
#### Postcondition:
The attendee’s information is updated in the registration portal.
#### Alternative Flows:
- **Validation Error**: If any of the entered details are invalid, the system displays an error message and prevents the update.

## Use Case 5: Event Organizer Views Attendee List
### Actor: Event Organizer/Admin
#### Precondition:
The event organizer must have access to the admin interface of the registration portal and be logged in.
#### Main Steps:
1. The organizer logs into the admin interface using their credentials.
2. They navigate to the registrations section where the list of attendees for the event is displayed.
3. They can filter or search for specific attendees based on name, email, or other criteria.
4. They view detailed information about each attendee and any additional notes added by them.
#### Postcondition:
The organizer has access to a comprehensive list of all registered attendees for the event.
#### Alternative Flows:
- **No Attendees Found**: If no registrations are found for the selected event, the system displays a message indicating that there are no attendees.

## Use Case 6: Event Organizer Sends Notification
### Actor: Event Organizer/Admin
#### Precondition:
The event organizer must have access to the admin interface of the registration portal and be logged in.
#### Main Steps:
1. The organizer logs into the admin interface using their credentials.
2. They navigate to the events section where they can select an event for which a notification is needed.
3. They compose a message or email that needs to be sent to all registered attendees for that event.
4. They choose the recipients (all attendees, specific category of attendees, etc.) and click on "Send" to broadcast the message.
5. The system confirms that the message has been successfully sent.
#### Postcondition:
All selected attendees receive the notification regarding the specified event.
#### Alternative Flows:
- **No Recipients Found**: If no attendees are found for the selected category, a message should inform the organizer accordingly.

These use cases cover various scenarios related to managing and interacting with the Event Registration Portal system.