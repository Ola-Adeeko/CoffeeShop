/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'ola-joshua.us', // 
    audience: 'coffee', // the audience set for the auth0 app
    clientId: 'sF7jkcdz5JK7xf89msPHB9uK137AaLmW', // the client id generated for the auth0 app
    callbackURL: 'https://localhost:8100/tabs/user-page', // the base url of the running ionic application. 
  }
};
