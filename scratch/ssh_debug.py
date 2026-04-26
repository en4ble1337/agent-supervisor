import asyncio
import asyncssh
import sys

async def test_ssh():
    ip = "10.1.20.191"
    user = "openclaw"
    pw = "n0d3!"
    
    print(f"--- SSH Debug Tool ---")
    print(f"Target: {user}@{ip}")
    print(f"Testing connection...")
    
    try:
        async with asyncio.wait_for(asyncssh.connect(
            ip,
            username=user,
            password=pw,
            known_hosts=None,
        ), timeout=10.0) as conn:
            print("SUCCESS: Connected successfully!")
            result = await conn.run("whoami", check=True)
            print(f"Remote user: {result.stdout.strip()}")
            
    except asyncio.TimeoutError:
        print("ERROR: Connection timed out (10s). The IP might be unreachable or firewalled.")
    except asyncssh.PermissionDenied:
        print("ERROR: Permission Denied. Username or password incorrect.")
    except asyncssh.HostKeyNotVerifiable:
        print("ERROR: Host key not verifiable.")
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_ssh())
