const fetch = require('node-fetch');
const sgMail = require('@sendgrid/mail');

exports.handler = async (event, context) => {
  // Hantera CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Hantera preflight OPTIONS request
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ message: 'CORS preflight' })
    };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { message, history = [] } = JSON.parse(event.body);

    if (!message) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Message is required' })
      };
    }

    // Azure OpenAI konfiguration
    const API_KEY = process.env.AZURE_OPENAI_API_KEY;
    const ENDPOINT = process.env.AZURE_OPENAI_ENDPOINT || "https://yazan-me7jxcy8-eastus2.cognitiveservices.azure.com/";
    const DEPLOYMENT_NAME = process.env.AZURE_OPENAI_DEPLOYMENT || "gpt-4.1";
    const API_VERSION = process.env.AZURE_OPENAI_API_VERSION || "2025-01-01-preview";

    if (!API_KEY) {
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Azure OpenAI API key not configured' })
      };
    }

    const url = `${ENDPOINT}openai/deployments/${DEPLOYMENT_NAME}/chat/completions?api-version=${API_VERSION}`;

    const systemMessage = {
      role: "system",
      content: `Optitech Sverige AI-support. Hjälp kunder direkt när möjligt. 
Vid komplexa problem som kräver ärendehantering, samla: namn, e-post, problembeskrivning.
Svara då: "SKAPA_ÄRENDE: [namn] | [email] | [beskrivning]" `
    };

    const messages = [systemMessage, ...history, { role: 'user', content: message }];

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'api-key': API_KEY
      },
      body: JSON.stringify({
        messages: messages,
        temperature: 0.3,    // Lägre temperatur för snabbare svar
        max_tokens: 800,     // Minska tokens för snabbare svar
        top_p: 0.9,          // Optimera för hastighet
        frequency_penalty: 0.1
      }),
      timeout: 15000  // 15 sekunders timeout
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Azure OpenAI Error:', response.status, errorText);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ 
          error: 'AI service temporarily unavailable',
          details: `Status: ${response.status}`
        })
      };
    }

    const data = await response.json();
    const aiReply = data.choices[0].message.content;

    // Kolla om AI vill skapa ett ärende
    const ticketPattern = /SKAPA_ÄRENDE:\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*(.+)/;
    const ticketMatch = aiReply.match(ticketPattern);

    let responseData = {
      success: true,
      response: aiReply,
      ticket_created: false
    };

    if (ticketMatch) {
      // Ta bort SKAPA_ÄRENDE delen från svaret
      const cleanResponse = aiReply.replace(ticketPattern, "").trim();
      if (cleanResponse) {
        responseData.response = cleanResponse;
      } else {
        responseData.response = "Jag skapar ett supportärende åt dig nu...";
      }

      // Generera ticket ID
      const timestamp = new Date().toISOString().slice(0, 10).replace(/-/g, '');
      const ticketId = `OPT-${timestamp}-${Math.random().toString(36).substr(2, 4).toUpperCase()}`;
      
      const ticketData = {
        namn: ticketMatch[1].trim(),
        email: ticketMatch[2].trim(),
        beskrivning: ticketMatch[3].trim()
      };

      responseData.ticket_created = true;
      responseData.ticket_id = ticketId;
      responseData.ticket_data = ticketData;

      // Skicka e-post via SendGrid
      const sendgridApiKey = process.env.SENDGRID_API_KEY;
      if (sendgridApiKey) {
        try {
          sgMail.setApiKey(sendgridApiKey);

          // E-post till kund
          const customerEmail = {
            to: ticketData.email,
            from: 'support@optitech-sverige.se',
            subject: `Vi har tagit emot ditt supportärende – ${ticketId}`,
            text: `Hej ${ticketData.namn},

Tack för att du kontaktade oss. Vi har tagit emot följande ärende:

${ticketData.beskrivning}

Ärendenummer: ${ticketId}

Vårt supportteam återkommer så snart som möjligt.

Vänliga hälsningar,  
Supportteamet`
          };

          // E-post till admin
          const adminEmail = {
            to: 'support@optitech-sverige.se',
            from: 'support@optitech-sverige.se',
            subject: `Nytt supportärende från ${ticketData.namn} – ${ticketId}`,
            text: `Ett nytt ärende har inkommit:

Namn: ${ticketData.namn}
E-post: ${ticketData.email}
Ärende:
${ticketData.beskrivning}

Ärendenummer: ${ticketId}`
          };

          // Skicka båda e-posten
          console.log('Attempting to send emails with SendGrid...');
          await Promise.all([
            sgMail.send(customerEmail),
            sgMail.send(adminEmail)
          ]);

          console.log('Emails sent successfully');
          responseData.email_sent = true;
        } catch (emailError) {
          console.error('Email sending failed:', emailError);
          console.error('SendGrid API Key exists:', !!sendgridApiKey);
          console.error('Error details:', emailError.response?.body || emailError.message);
          responseData.email_sent = false;
          responseData.email_error = emailError.message;
        }
      } else {
        console.error('SendGrid API key not found in environment variables');
        responseData.email_sent = false;
        responseData.email_error = 'SendGrid API key not configured';
      }
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(responseData)
    };

  } catch (error) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Internal server error',
        message: error.message 
      })
    };
  }
};
