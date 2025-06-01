//Types
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

interface TransactionFields {
    "USD": number;
    "Notes": string;
    "Date": string;
    "Vendor": string;
    "Name": string;
}

interface Transaction {
    id: string;
    createdTime: string;
    fields: TransactionFields;
}

export interface Transactions {
    data: Transaction[];
}

interface AccountFields {
    "USD": number;
    "Institution": string;
    "Last Successful Update": string;
}

interface Account {
    id: string;
    createdTime: string;
    fields: AccountFields;
}

export interface Accounts {
    data: Account[];
}