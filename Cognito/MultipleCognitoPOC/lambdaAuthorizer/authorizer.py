import json
import jwt
import base64

def authorizer(event, context):
    
    effect = "Deny"

    try:
        valid_userpools = ["https://cognito-idp.us-east-1.amazonaws.com/us-east-1_jCOnOGPsz", "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_NsKXmRvr9", "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_h6iqBsTk4"]

        public_keys = {"https://cognito-idp.us-east-1.amazonaws.com/us-east-1_jCOnOGPsz": json.loads("""{"keys":[{"alg":"RS256","e":"AQAB","kid":"NIzLZv+LlgaFmwy3A2GuBZeMZdygwuSFKp+JjhAeOP0=","kty":"RSA","n":"05uIHPkfpevCuw08wAJEF4ynQj8PW3VC-BnhKDer9A9gXyPBKU3v2Uy2GRmZPQexXJKolD03fSoTkqQCmROtIW6KG8bCG05PnO1k73321tAXA0h9trqTqKYkdmkQ9blJzZ178GU8y0vuxgw582HzUtFUkVstX6k9jwzFxDi3TLK0DBWhWkHPo84tNJHMP8rgeSNt2hsPHlYO_r4g1XRmArwqrXMG-l4tb1tB3yKxUo6454GE1UdyEW-MH2jcKU9UHAjF_suGkIiXgnaFmY1Qawy_vKl_O-xkdEplbJksO8OXO_LlcJKGZc_5ZetjSi6wYvzyp07PQTrmo-CubFvQow","use":"sig"},{"alg":"RS256","e":"AQAB","kid":"BKO3ycC2L/09F0vOhv1lhiskvZjEM7FUXF/hxSCafTk=","kty":"RSA","n":"v1XofRUpK1eHj_VsWgWahWzXR57pW-PTXlRNI-CMYa9NF1KfnTTYX9dEpB0qAYX2Bxox2hfstBgtHGd-yomX9xucoy08sHOa4Gdqbp2kBSAJQ_Z69tcnVt_fDrNV-Tw_TXaFLxjteKkQ9RbWMLzxAKE6Cz3Be9J4fXlNG4_l6eulaTYKRYnNx43fhN8xJ1QBNj7KtolTOFkkz-egugSn3Lre-00E4pidO4U3_qA0BnLnkY9chVln9VhGeGdrHaHClelPwRryDTDCUsRFM1vkSZEtc5CKWUS2R13atCmVdAnNe-BpmOFvHt5o9hH6nKvCOdThNV2xSbHTOt4TojwHYw","use":"sig"}]}"""),
            "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_NsKXmRvr9": json.loads("""{"keys":[{"alg":"RS256","e":"AQAB","kid":"9T+zmlZbrzqJf04AgGEkfOC3ARFxp8f44OZcl0qS1SY=","kty":"RSA","n":"1OHBN6OFTKDuQzgeFmovc6Gjg5lt_xWxiomA9-OSM2CrhQaC6WHilVMf0zJdh90jXu1LHtwjNgLwfK4EQoHn4OHGhk-iO63w1AOVnCkyNRpP3Pwzp3O7tVno6D6SI8tW4cgUrKgram0ZlsyFRP9W5ltHJoxVQLoZBNnTTSfD88aJm7JOYhAwrsTGuAiRFIbte4g0zCdkOwioRV4EnxRGwIiAmzV57C55ep4nkjodxvm_M7MTLQTxaBbIGaj8lMP0O3M5NTE1LhQ5d_mO4Z1U6Zq12eFDvg8uJipNdffG6TENNrdr2X1reJ2bnIPsGaGKy0fPO-0T9xJaN_4Vd_zw-w","use":"sig"},{"alg":"RS256","e":"AQAB","kid":"5vLPx5j0/GYajtK/0bQhtrdB2zQH8S+HKJ6zidNEKqI=","kty":"RSA","n":"rCjzgtE9Jny5y7UbTzGiF_DnyJ6wedEx-0fC26snrGk18vxYKQSC1L6MbzBnnAjiaf30ByRv2acem1CCPToVfTB-6JhTNawSVA6yPg0RJzVhbtTHvKYJxaNJiOwJVhdTpgsGH2tJIDyUU83kZpZwoz6UlBFKu4JoJLIip5p5GY7Tiu-4Ego2ADX54L6g8gM05JHDvfefYaYIyLRJeaiPsF8CqBXMoNVe3yydyOfXEseUGiVH2vDeSBcOkOZkB0LaitKl7uvy6-hnOIXAqjXyE_ae2hEAPpqQ3q3rN6f-6WhBrwmafXvGA9Drq42hT0SUhpr7FGFKbYzzDw0NL2GLZQ","use":"sig"}]}"""),
            "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_h6iqBsTk4": json.loads("""{"keys":[{"alg":"RS256","e":"AQAB","kid":"8Wc+v04HeQ2rWHQKghNPRcK14nDRnRj3YVfwib9wwgo=","kty":"RSA","n":"r6XzI8AFLTEMLrk1kR_ALsUaqL22ZI30JV74SRayLMQoADpQPdVHXv0E6L8ZUcsWI-B69PXS-6G83IReasmtEDQrycP2f6OjjyN0hwmMcXkM82SsyxJ57XfJiIyI6W5tKdVz2VFMWqlj2fgnpXMm0VVDvqsXqjeTKLq-BLKm4E0i_I5P5W8MCIBr49p6aYknxXCV1rGMSpmNu6blYtktuHuFjSQ2NRfzlq2em1TUiI9DDYpDZ9guOLylxgWTy0oMZxiQR8-U2WOUQBC5AJDIU9SCxaWZbXdq-VkRE2oKqAy58VoMHH-oktkOMwHgGAuvZUTT1HMdGSO2no2R_5jBZQ","use":"sig"},{"alg":"RS256","e":"AQAB","kid":"XWVc53B+v/zizuHFikbuuUjwTYcz3JsD3UfqVxCoTew=","kty":"RSA","n":"w-e0YBpqamiy_zY-pkO8Qo6hLYIcRilkvBhXpHyzGa7qthCRcxgNm4videAznhZdh4WgOJgOseEgTELxV0DJUMyU47mOqeM8-ewoVMOkDaqBmwC-MeUlHQPNBeHWbFYW-fADAo-WUpYRgbDCiT-VQEv0Ux3flXmDal4sNuahSjDz3OqIvNlnQTQUGzQC0DJcqFhWqCTDTl2h1Fh5CtgDe68lSGN3WW1rdWNwQ-MkcBLr_xY6QxGozPlDD4U5Z0-PY8md2Dk-tMAZgNk5bhUxiSlP7ORgKdELSpbzMy4qJA23zqs_1YHCgiXCbuXzzK7kq1X51lUo1LgF0-g3IdXRxQ","use":"sig"}]}""")
        }

        token = event.get('authorizationToken').replace("Bearer ", "")
        kid = jwt.get_unverified_header(token)['kid']
        issuer = jwt.decode(token, options={"verify_signature": False})['iss']
        username = jwt.decode(token, options={"verify_signature": False})['cognito:username']
        aud = jwt.decode(token, options={"verify_signature": False})['aud']

        if issuer in valid_userpools:
            if kid == public_keys[issuer]["keys"][0]["kid"]:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(public_keys[issuer]["keys"][0])
                decoded = jwt.decode(token, public_key, audience=aud, algorithms=["RS256"])
            elif kid == public_keys[issuer]["keys"][1]["kid"]:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(public_keys[issuer]["keys"][1])
                decoded = jwt.decode(token, public_key, audience=aud, algorithms=["RS256"])
            else:
                raise Exception("not valid kid")
            effect = "Allow"
        else:
            raise Exception("userpool not in list")

    except Exception as e:
        print(str(e))
        effect = "Deny"

    policy = {
        'principalId': 'user',
        'policyDocument': {
            'Version': "2012-10-17",
            'Statement': [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": event.get('methodArn')
                }
            ]
        }
    }

    return policy