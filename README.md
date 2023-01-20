# library

# Domain description and rules

## Presentation

The domain aims at representing a library with book references and copies of them bound to be borrowed by people. So First of all, the system manages books and authors.

An author MAY be author of several works which MAY have been published in different books references according to publishing background. In this example, we gonna have a simple way not considering the work by itself in its universal description, but directly & link between author and book.

So, an **Author** MAY be author of several **Books**. 
A **Book** MAY have several **Authors**
An **Author** is described by his name
A **Book** is described by its title, the list of **Authors** of the work, the ISBN (International Standard Book Number) which is an unique identifier for a published version of a **Book**. Two **Books** MUST NOT have the same ISBN.
An **Author** MUST NOT be removed from the system till the system contains a **Book** written by the **Author**.

The main goal of a library is to give people access to works. So it has to own copies of books in order they are borrowed. Copies are well tidied and ordered on shelves.

So a **Copy** references the book it is a copy of, and the place where it MUST be tidied in the library. A **Book** CAN NOT be removed from the system till the library owns a **Copy** of the **Book**.

Finally copies MAY be borrowed by people, a **Checkout** manages this considering the borrower, the date of **Checkout** creation, the date of expected book return. By defautl a book is borrowed for 10 days. A prolongation MAY be done on an existing borrow.

A book MUST be returned to the library and MUST NOT be directly switched to another **Checkout**. A new **Checkout** MUST only be performed on an available copy, that is to say not on a copy that should be already borrowed.

## Representation

Find below the schema of the previously described concepts


# API endpoints

## Author resource

## Book resource

## Copy resource

## Checkout resource



# Run application

Launche application via uvicorn http server

```uvicorn main:app --reload```



