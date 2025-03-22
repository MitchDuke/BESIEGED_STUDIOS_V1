#   Project Concept
Title: Miniature Painting Commission Website (Besieged Studios)

##  External User's Goal:
Commission a custom miniature painting service tailored to their preferences and budget.

##  Site Owner's Goal:
Earn revenue by showcasing prior work, receiving commissions, and managing client interactions efficiently.

##  Features and Functionalities
  - Core Features
  - Gallery/Portfolio:

  - Display completed miniature projects categorized by type (e.g., fantasy, sci-fi, dioramas).
    - Showcase testimonials from satisfied clients alongside project images.

  - Commission Form with Quote Calculator:
    - Allow users to specify their miniature painting needs, including:
      - Type of miniature (e.g., single figure, squad, diorama).
      - Size (e.g., 28mm scale, 54mm scale).
      - Level of detail (tabletop standard, display standard, competition standard).
  - Provide a live quote preview using JavaScript.
  - Ensure the final quote is calculated securely on the server.

  - User Accounts:
    - Enable users to create accounts to track their commission status and access completed works.

  - E-Commerce Integration:
    - Integrate Stripe to handle payments for commission deposits or full orders.

  - Order Management (Admin Dashboard):
    - Allow the site owner to manage orders:
    - View and update order status (e.g., "Pending", "In Progress", "Completed").
    - Upload photos of the completed miniature for client review.
    - Approve or reject client requests for revisions.

  - Feedback Mechanism:
    - Allow clients to accept the finished miniature or request minor adjustments.
    - Once accepted, clients can submit a testimonial that gets displayed on the site.

##  Advanced Features (Nice-to-Have)
  - Custom Gallery Display:
    - Create an interactive, JavaScript-powered carousel or grid with filters (e.g., by category, painting level).
    
  - Dynamic Pricing Adjustments:
    - Include optional add-ons (e.g., custom bases, weathering effects) that dynamically update the quote.

##  Project Structure

  - Apps

    - Gallery App:
      - Manages the display of completed works and testimonials.

    - Commission App:
      - Handles commission requests, orders, and payments.

    - Authentication App:
      - Manages user registration, login, and profiles.

    - Admin Dashboard App:
      - Provides a management interface for the site owner.


##  Testing

  - Stripe:
    - To test the Stripe payment system the following test scenarios were used:
      - Successful payment Card Number: 4242 4242 4242 4242
      - Failed payment Card Number: 4000 0000 0000 0002 (Declined payment)
      - Authentication Required (3D Secure) Card Number: 4000 0025 0000 3155 (Requires extra authentication)
      - Insufficient Funds Card Number: 4000 0000 0000 9995
    - Using the above card numbers, any future expiry date, any 3 digit CVC number and a valid postcode.
