# Security and privacy

The viewer reads a real camera and can save video of real people. The design keeps that data on the local machine and makes recording visible. This page explains the choices and their limits. It does not give legal advice. The words used here are defined in [GLOSSARY.md](../../GLOSSARY.md).

## Consent

Use a camera you own or have permission to use. Record only places and people who agreed to be recorded. The implementation guide states this as a rule, and it applies to every test, demo and normal run. A recording feature is easy to leave running by accident, so consent has to be settled before the stream starts.

## Local storage

Screenshots go to `screenshots/` as JPEG files. Recordings go to `recordings/` as MP4 files. Both folders sit next to the project on the same machine. The code sends no media to a server, a cloud bucket or a third-party service. There is no telemetry and no analytics client.

The only network traffic is local. `check_reachable` makes one short HTTP request to the camera before the stream opens. `open_capture` then reads the MJPEG stream from the same address. Nothing else leaves the laptop.

## Visible recording state

While a `VideoWriter` is active, the window shows a red circle near the top right and the text `REC {elapsed}s` beside it. Both manual recordings started with `R` and motion recordings show this badge. A person who can see the screen can see that recording is on. The counter uses whole seconds from the writer's start time.

## Files kept out of Git

`.gitignore` excludes `recordings/`, `screenshots/`, `.env` and `*.log`. A commit would make footage and the camera address public and permanent, and deleting a file in a later commit would not remove it from history. Keeping these paths out of the repository is the decision in [ADR-0001](../adr/0001-keep-camera-secrets-out-of-git.md).

The real address lives in `.env`. `.env.example` carries only `https://<phone-ip>:8080/video`. Console messages and log lines name the problem without printing the full address. Test evidence is held to the same rule: a screenshot must hide the address and any credentials before it is shared.

## Retention

The code does not delete files. Once written, a recording or screenshot stays until someone removes it. Retention is therefore a user decision. Review the two folders and delete files when the reason for keeping them ends. Nothing in the viewer enforces a time limit, so a long-running setup can fill the disk.

## TLS on a trusted network

`CAMERA_VERIFY_SSL` defaults to `false`. IP Webcam serves HTTPS with a certificate the phone signs for itself, so both Requests and FFmpeg reject it by default. With the setting false, Requests skips verification and FFmpeg gets `tls_verify;0`. The viewer connects to the address the app shows without importing a certificate.

The trade-off is real. Anyone with access to the same local network could impersonate the camera and serve frames to the viewer. Use the setting on a trusted local Wi-Fi only. A user who installs the phone's certificate can set `CAMERA_VERIFY_SSL=true` and get verification back. See [ADR-0005](../adr/0005-handle-the-self-signed-certificate.md).

## Data protection law

Kenya's Data Protection Act is a consideration to check, not a legal claim made here. Video of identifiable people can count as personal data. Before recording people, check the current law and what it asks of you: the reason for recording, who may view it, how long it is kept, and what happens to it after deletion. The project gives no legal conclusion and makes no claim about which obligations apply to a given user.

## Limits of the design

The viewer has no encryption at rest. Anyone with access to the folder can open the files. There is no login on the viewer, no per-file access control, no redaction of faces or plates, and no audit log of who watched a stream. The REC badge marks active recording but does not tell people outside the room. These are known limits, not hidden behaviour. Add controls before using the tool where these properties matter.
