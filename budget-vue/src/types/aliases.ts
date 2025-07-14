/**
 * Model/Type Dfeinitions
 */


//Definitions**************************
interface TransactionFields {
    "USD": number;
    "Notes": string;
    "Date": string;
    "Vendor": string;
    "Name": string;
    "Account ID": string;
}
interface Transaction {
    id: string;
    createdTime: string;
    fields: TransactionFields;
}
interface AccountFields {
    "USD": number;
    "Institution": string;
    "Last Successful Update": string;
    "Plaid Account ID": string;
}
interface Account {
    id: string;
    createdTime: string;
    fields: AccountFields;
}


//Exports**************************
export interface Accounts {
    data: Account[];
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
export interface Transactions {
    data: Transaction[];
}