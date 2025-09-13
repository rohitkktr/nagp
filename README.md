# NAGP Microservices Project

This repository contains a microservices-based project with the following services:

## Services

1. **Auth Service**
   - Handles user authentication.
   - Endpoints:
     - `POST /login`: Authenticates a user.

2. **Cart Service**
   - Manages user shopping carts.
   - Endpoints:
     - `POST /cart/{username}/add`: Adds an item to the user's cart.
     - `GET /cart/{username}`: Retrieves the user's cart.
     - `DELETE /cart/{username}/clear`: Clears the user's cart.

3. **Order Service**
   - Processes user orders.
   - Endpoints:
     - `POST /order`: Places an order for the user.

4. **Product Service**
   - Provides product information.
   - Endpoints:
     - `GET /products`: Retrieves available products with optional filters for name and category.

5. **Nagp Frontend**
   - A SvelteKit-based frontend for the microservices.
   - Hosted on S3.
   - Build, deploy, and local run instructions:
     ```bash
     # Navigate to the frontend directory
     cd nagp-frontend

     # Install dependencies
     npm install

     # Run the project locally
     npm run dev

     # Build the project
     npm run build

     # Deploy to S3
     aws s3 sync build/ s3://<your-s3-bucket-name> --delete
     ```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd nagp
   ```

3. Build and run the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Access the services at `http://localhost:<port>` where `<port>` is the port specified for each service in the `docker-compose.yml` file.

## Dependencies

Each service has its own `requirements.txt` file for Python dependencies. These are automatically installed when using Docker.

## Testing Endpoints in Postman

You can use the following endpoints to test the services in Postman. Replace `<base_url>` with `http://localhost` and the respective port for each service.

### Auth Service
- **Login**
  - Method: `POST`
  - URL: `<base_url>:8000/login`
  - Body (JSON):
    ```json
    {
      "username": "<username>",
      "password": "<password>"
    }
    ```

### Cart Service
- **Add to Cart**
  - Method: `POST`
  - URL: `<base_url>:8002/cart/{username}/add`
  - Body (JSON):
    ```json
    {
      "product_id": <product_id>,
      "quantity": <quantity>
    }
    ```
- **Get Cart**
  - Method: `GET`
  - URL: `<base_url>:8002/cart/{username}`
- **Clear Cart**
  - Method: `DELETE`
  - URL: `<base_url>:8002/cart/{username}/clear`

### Order Service
- **Place Order**
  - Method: `POST`
  - URL: `<base_url>:8003/order`
  - Body (JSON):
    ```json
    {
      "username": "<username>"
    }
    ```

### Product Service
- **Get Products**
  - Method: `GET`
  - URL: `<base_url>:8001/products`
  - Query Parameters (Optional):
    - `name`: Filter by product name
    - `category`: Filter by product category

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.