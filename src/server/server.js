const express = require('express');
const cors = require('cors');
// library for generating symmetric key for jwt
const { createSecretKey } = require('crypto');
// library for signing jwt
const { SignJWT } = require('jose-node-cjs-runtime/jwt/sign');
// library for verifying jwt
const { jwtVerify } = require('jose-node-cjs-runtime/jwt/verify');

const app = express();

app.use(cors());

app.use('/login', (req, res) => {
	res.send({
		token: test123
	});
});

app.listen(8080, () => console.log('API running on port 8080'))