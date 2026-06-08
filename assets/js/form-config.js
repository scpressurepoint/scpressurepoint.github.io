/* Form delivery config — static site (GitHub Pages)
 *
 * DEFAULT (works out of the box, no signup):
 *   Hero quote, estimate, and survey forms open the visitor's text app with
 *   details pre-filled to phone below. Nothing else to configure.
 *
 * OPTIONAL EMAIL via Web3Forms (free, ~2 min setup for Parker):
 *   1. Go to https://web3forms.com
 *   2. Enter scpressurepoint@gmail.com → click "Create Access Key"
 *   3. Open the confirmation email and copy the access key (check spam)
 *   4. Paste it into web3formsAccessKey below
 *   5. Commit and push — forms email you first; if delivery fails, text fallback still works
 */
window.SC_FORM_CONFIG = {
  phone: '8032728118',
  thankYouPath: 'pages/thank-you.html',
  web3formsAccessKey: ''
};
