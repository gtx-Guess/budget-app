//Types

export interface PlaidUser {
    id: string;
}

export interface LoginApiResponse {
    status: Number;
    data: {
        message: string;
    };
}

export interface User {
    first_name: string;
    last_name: string;
    email_address: string;
}