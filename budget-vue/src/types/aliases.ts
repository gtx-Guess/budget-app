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