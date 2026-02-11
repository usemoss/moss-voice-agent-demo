import { NextResponse } from 'next/server';
import { MossVoiceServer } from '@moss-tools/voice-server';

type ConnectionDetails = {
  serverUrl: string;
  roomName: string;
  participantName: string;
  participantToken: string;
};

// Cache the initialization promise to prevent race conditions with concurrent requests
let voiceServerPromise: Promise<MossVoiceServer> | null = null;

async function getVoiceServer(): Promise<MossVoiceServer> {
  if (!voiceServerPromise) {
    voiceServerPromise = MossVoiceServer.create({
      projectId: process.env.MOSS_PROJECT_ID!,
      projectKey: process.env.MOSS_PROJECT_KEY!,
      voiceAgentId: process.env.MOSS_VOICE_AGENT_ID!,
    }).then((instance) => {
      console.log('✅ MossVoiceServer instance created and cached');
      return instance;
    });
  }
  return voiceServerPromise;
}

export async function POST(req: Request) {
  try {
    const voiceServer = await getVoiceServer();

    // Parse agent configuration from request body
    const body = await req.json();
    const agentName: string = body?.room_config?.agents?.[0]?.agent_name;
    console.log(`Received request for agent: ${agentName}`);

    // Generate participant token
    const participantName = 'user';
    const participantIdentity = `voice_assistant_user_${Math.floor(Math.random() * 10_000)}`;
    const roomName = `voice_assistant_room_${Math.floor(Math.random() * 10_000)}`;

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
