#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>
#include <iostream>

int main(int argc, char* argv[]) {
    if (!SDL_Init(SDL_INIT_VIDEO | SDL_INIT_CAMERA)) {
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow("AI Sign Language Translator", 960, 640, SDL_WINDOW_RESIZABLE);
    if (!window) {
        SDL_Quit();
        return 1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, nullptr);
    if (!renderer) {
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    int camera_count = 0;
    SDL_CameraID* cameras = SDL_GetCameras(&camera_count);
    SDL_Camera* camera = nullptr;

    if (!cameras || camera_count == 0) {
        std::cerr << "No webcam detected on the current device." << std::endl;
        SDL_ShowSimpleMessageBox(SDL_MESSAGEBOX_WARNING, "Webcam", "No webcam detected on the current device.", window);
    } else {
        camera = SDL_OpenCamera(cameras[0], nullptr);
    }
    SDL_free(cameras);

    bool running = true;
    SDL_Event event;
    SDL_Texture* texture = nullptr;

    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_EVENT_QUIT || (event.type == SDL_EVENT_KEY_DOWN && event.key.key == SDLK_ESCAPE)) {
                running = false;
            }
        }

        if (camera) {
            Uint64 timestampNS = 0;
            SDL_Surface* frame = SDL_AcquireCameraFrame(camera, &timestampNS);
            if (frame) {
                if (texture) {
                    SDL_DestroyTexture(texture);
                }
                texture = SDL_CreateTextureFromSurface(renderer, frame);
                SDL_ReleaseCameraFrame(camera, frame);
            }
        }

        SDL_SetRenderDrawColor(renderer, 24, 28, 36, 255);
        SDL_RenderClear(renderer);

        if (texture) {
            SDL_RenderTexture(renderer, texture, nullptr, nullptr);
        }

        SDL_RenderPresent(renderer);
        SDL_Delay(16);
    }

    if (texture) {
        SDL_DestroyTexture(texture);
    }
    if (camera) {
        SDL_CloseCamera(camera);
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
