# onfabric

## Full Stack Take Home Test

### Intro

Congratulations on being selected to take the onfabric full-stack take home test. This project is carefully devised to test your understanding and experience of full-stack development. We've opted for a stack that remembles the onfabric stack:

- `/frontent` is a `typescript+nextjs` app
- `/backend` is a `python+FastAPI` api

### Getting started

To run locally, make sure your docker daemon is running, and run the following in the root of the project.
```
> docker-compose up
```

After which you will be able to visit:

- `http://localhost:3000` for the next app, and
- `http://localhost:8080/api/v1/docs` for the backend api docs.

If you can't get to this point, there's no shame in reaching back out to us for some help--there's a chance we misconfigured something, or overlooked an OS.

If you wish to run the next app outside of the docker container you'll need to:

```
> cd frontent
> npm i
> npm run dev
```

or FastAPI

```
> cd backend
> # set-up the pipenv environment
> pip install pipenv
> pipenv shell
> # install and run
> pipenv install
> pipenv run dev
```

### Testing

You'll notice a directory `/backend/tests`, you can run all the tests by simply running:

```
> cd backend
> pytest
```

To do this you'll need to make sure you have set-up your pipenv environment.

If you change any code, it's likely you'll need to add / edit a test.

### What am I looking at?

This is a very basic app. There are three models (`/backend/app/models.py`):

- `User` - The user, an entity that can make requests;
- `ApiKey` - The key's that allow users to make requests;
- `UserRequest` - Requests the user has made with an API key.

You'll find the `CRUD` operations related to these models here: `/backend/app/crud.py`.

You'll find the api routes here: `/backend/app/api/routes/`.

And the schemas (pydantic models) that defined the api interfeces here: `/backend/app/schema.py`.

I'll spare you an explaination of the frontend as there's nothing special going on there. If you have no idea what you're looking at I reccomend going and reading the first page of the `next` docs for app router. If you're familair with react you should have no issues.

You will notice that a `Dashboard Key : 6471f3f8-c742-4e21-9bd8-f2bf4d07eb3a` comes stock with the app, this is what the `next` app uses to make the requests, so you will see a lot of requests associated with it (as the next app is making these requests). If you wish to see logs for any of the other api keys you may create, you'll need to either make the requests manually - or use the docs to "Try it out".

### Before we begin

We're not primarily interested in how well you know `next` or `fastapi`. If you're a next pro, you'll notice that (almost) all the components in the `next` app are client components. This is to not disadvantage anyone who might be a react wiz, but not familair with RSC and `next`. We're trying to get a feeling for how well you understand the relationship between the server and the client, and if you can take requirements and turn them into code.

Please don't spend more than 3-4 hours on this. If you can't get through all the tasks, that's fine.

Feel free to add any additional packages to help you complete the tasks (though no additional packages are required).

Good luck!

## Tasks

### Task 1: Warm-up

A test is broken, fix it.

### Task 2: Better request logging

Currently, we're not logging a lot in the `UserRequests`, can you:

- Add what you think might be approprioate to log in the user requests
- Update the API interface to expose these new fields to the frontend
- Update the types / table columns in the front end to show these new fields.

### Task 3: Pagination

You will have noticed by now that we are reading in _a lot_ of data when we ask for the user requests. You're job is to paginate the user requests so the client only has 10 items in the state at a time.

(If you're not familair with `sqlalchemy` you might want to look at the methods `offset` and `limit`).

### Task 4: Polling

When we make requests with a key, we don't see the change in the UI until we reload the page or toggle selected api keys. While an api key is selected, poll the user requests for that key every 5 seconds. We should be able to see in the UI that we are re-fetching the requests.

### Task 5: User requests download

Add the ability to download the user requests table from the frontend as a csv.

### Task 6: Order requests by duration

Add the ability to sort the table by request latency. Don't worry about editing the `Table` component, a toggle above the table is fine.

### Task 7: Charts (optional if you have time)

With a charting library of your choice, visualise the request latency in a chart below the `userRequest` table. Determine the most useful visualisation of this data.

## Thanks!
When you're done with the task, create a new (private) github repo and add @jskerman + fire through an email notifying us that you're complete and ready for review.
