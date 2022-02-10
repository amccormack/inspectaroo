#!/bin/bash
rm -f .env
aws sts assume-role --role-arn 'arn:aws:iam::248812944192:role/inspectaroo-user-dev' --role-session-name amtest | \
		jq '.Credentials| [.AccessKeyId, .SecretAccessKey, .SessionToken]' | \
		jq '@sh "export INS_ACCESS_KEY=\(.[0]);export INS_SECRET_ACCESS_KEY=\(.[1]);export INS_SESSION_TOKEN=\(.[2])"' -r | \
		tr ';' '\n' > .env