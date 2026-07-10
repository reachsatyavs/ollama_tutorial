Certainly! Below is a class diagram for an Event Registration Portal using Mermaid syntax. The diagram includes main classes, properties, methods, and relationships such as inheritance and associations.

```mermaid
classDiagram
    class User {
        - userId: String
        - username: String
        - email: String
        - passwordHash: String
        + register(email: String, password: String): Boolean
        + login(username: String, password: String): Boolean
        + logout(): void
    }

    class Admin extends User {
        + approveEvent(eventId: String): Boolean
        + rejectEvent(eventId: String): Boolean
        + deleteUser(userId: String): Boolean
    }

    class Event {
        - eventId: String
        - eventName: String
        - eventDate: Date
        - location: String
        - capacity: Integer
        - registrationCount: Integer
        + registerUser(user: User): Boolean
        + unregisterUser(user: User): Boolean
        + isFull(): Boolean
    }

    class Registration {
        - registrationId: String
        - userId: String
        - eventId: String
        - registrationDate: Date
        + validateRegistration(): Boolean
    }

    class Payment {
        - paymentId: String
        - registrationId: String
        - amount: Double
        - paymentDate: Date
        + processPayment(): Boolean
    }

    User "1" -- "*" Registration: makes
    Admin "1" -- "*" Event: manages
    Event "1" -- "*" Registration: has
    Registration "1" -- "1" Payment: involves

    class Organizer {
        - organizerId: String
        - organizerName: String
        - contactEmail: String
        + createEvent(eventName: String, date: Date, location: String, capacity: Integer): Event
    }

    User "1" -- "*" Organizer: is
```

### Explanation:

- **User**: 
  - Properties: `userId`, `username`, `email`, `passwordHash`
  - Methods: `register()`, `login()`, `logout()`

- **Admin**:
  - Inherits from `User`
  - Additional methods: `approveEvent()`, `rejectEvent()`, `deleteUser()`

- **Event**:
  - Properties: `eventId`, `eventName`, `eventDate`, `location`, `capacity`, `registrationCount`
  - Methods: `registerUser()`, `unregisterUser()`, `isFull()`

- **Registration**:
  - Properties: `registrationId`, `userId`, `eventId`, `registrationDate`
  - Method: `validateRegistration()`

- **Payment**:
  - Properties: `paymentId`, `registrationId`, `amount`, `paymentDate`
  - Method: `processPayment()`

- **Organizer**:
  - Properties: `organizerId`, `organizerName`, `contactEmail`
  - Method: `createEvent()`

### Relationships:
- A user can make multiple registrations (`User "1" -- "*" Registration`)
- An admin manages multiple events (`Admin "1" -- "*" Event`)
- An event has multiple registrations (`Event "1" -- "*" Registration`)
- A registration involves one payment (`Registration "1" -- "1" Payment`)
- A user is associated with one organizer (`User "1" -- "*" Organizer`)

This diagram provides a comprehensive view of the entities and their interactions within an Event Registration Portal.