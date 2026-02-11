import { NextResponse } from 'next/server';
// import { AccessToken, type AccessTokenOptions, type VideoGrant } from 'livekit-server-sdk';
// import { RoomConfiguration } from '@livekit/protocol';
import { MossVoiceServer } from "@moss-tools/voice-server";

// --------------------------


// Create participant tokens
// --------------------------

type ConnectionDetails = {
  serverUrl: string;
  roomName: string;
  participantName: string;
  participantToken: string;
};

// NOTE: you are expected to define the following environment variables in `.env.local`:
// const API_KEY = process.env.LIVEKIT_API_KEY;
// const API_SECRET = process.env.LIVEKIT_API_SECRET;

// don't cache the results
export const revalidate = 0;

export async function POST(req: Request) {
  try {


    // Parse agent configuration from request body
    const body = await req.json();
    const agentName: string = body?.room_config?.agents?.[0]?.agent_name;

    // Generate participant token
    const participantName = 'user';
    const participantIdentity = `voice_assistant_user_${Math.floor(Math.random() * 10_000)}`;
    const roomName = `voice_assistant_room_${Math.floor(Math.random() * 10_000)}`;
    const voiceServer = await MossVoiceServer.create({
    projectId: process.env.MOSS_PROJECT_ID!,
    projectKey: process.env.MOSS_PROJECT_KEY!,
    voiceAgentId: process.env.MOSS_VOICE_AGENT_ID!,
  });
  console.log(`✅ -> Voice server created: ${voiceServer.getServerUrl()}`);
    const participantToken = await voiceServer.createParticipantToken(
      { identity: participantIdentity, name: participantName },
      roomName,
      agentName
    );

    // Return connection details
    const data: ConnectionDetails = {
      serverUrl: voiceServer.getServerUrl(),
      roomName,
      participantToken: participantToken,
      participantName,
    };
    const headers = new Headers({
      'Cache-Control': 'no-store',
    });
    return NextResponse.json(data, { headers });
  } catch (error) {
    if (error instanceof Error) {
      console.error(error);
      return new NextResponse(error.message, { status: 500 });
    }
  }
}


