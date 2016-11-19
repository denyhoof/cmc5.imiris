#include <bits/stdc++.h>

using namespace std;

typedef int s_id;

struct StatManager
{
    double last_update_q = 0;
    set <s_id> status;
    map <s_id, double> data_start;
    double mid_size = 0;
    double time_service_q = 0;
    double time_service_food = 0;
    double slowpoke_time = 0;
    int max_students = 0;
};

int main()
{
    map <string, StatManager> res;

    double cur_time = 0;

    double all_students = 0;
    int all_students_cur = 0;
    int max_students = 0;
    double all_last_update = 0;

    map <s_id, double> start_time;
    map <s_id, double> total_time;

    while (cin >> cur_time){
        string buf;
        // :
        cin >> buf;
        // cur_id
        s_id cur_id = 0;
        cin >> cur_id;
        // Start or task
        cin >> buf;
        if (buf == "Start"){
            start_time[cur_id] = cur_time;
            cin >> buf;
            cin >> buf;
            //we do it in "wait"!
        } else if (buf == "task") {
            cin >> buf;
            // read status
            string status;
            cin >> status;
            if (status == "wait"){
                //calculate how long people stands in line before this student
                res[buf].mid_size += (cur_time - res[buf].last_update_q) * res[buf].status.size();
                res[buf].status.insert(cur_id);
                res[buf].data_start[cur_id] = cur_time;
                res[buf].last_update_q = cur_time;
                res[buf].max_students = max(res[buf].max_students, int(res[buf].status.size()));
                //update global stat
                all_students += (cur_time - all_last_update) * all_students_cur;
                ++all_students_cur;
                max_students = max(max_students, all_students_cur);
                all_last_update = cur_time;
            } else if (status == "service"){
                //read time for service
                double stime = 0;
                cin >> stime;
                res[buf].time_service_food += stime;
                res[buf].time_service_q += cur_time - res[buf].data_start[cur_id];
                res[buf].slowpoke_time = max(res[buf].slowpoke_time, cur_time - res[buf].data_start[cur_id]);
                //undate mid stat
                res[buf].mid_size += (cur_time - res[buf].last_update_q) * res[buf].status.size();
                res[buf].status.erase(cur_id);
                res[buf].last_update_q = cur_time;

                //update global stat
                all_students += (cur_time - all_last_update) * all_students_cur;
                --all_students_cur;
                all_last_update = cur_time;

                if (buf == "cash"){
                    total_time[cur_id] = cur_time + stime - start_time[cur_id];
                }
            } else if (status == "complete"){
                //do nothing, we do it in "service" case
            } else {
                cout << "Error reading status in time " << cur_time << endl;
                return -1;
            }
        } else {
            cout << "Invalid status in time " << cur_time << endl;
            return -1;
        }
    }
    for (auto node: res){
        cout << std::fixed << setprecision(6) <<  "status for elem: " << node.first << endl;
        cout << std::fixed << setprecision(6) << "    max_students: " << node.second.max_students << endl;
        cout << std::fixed << setprecision(6) << "    aver_students: " << node.second.mid_size / cur_time << endl;
        cout << std::fixed << setprecision(6) << "    aver_time_for_queue: " << node.second.time_service_q / node.second.data_start.size() << endl;
        cout << std::fixed << setprecision(6) << "    aver_time_total_in_stage: " << node.second.time_service_q / node.second.data_start.size() +
                                                 node.second.time_service_food / node.second.data_start.size() << endl;
        cout << std::fixed << setprecision(6) << "    student_that_wait_max: " << node.second.slowpoke_time << endl;
        cout << std::fixed << setprecision(6) << "    total_students_use: " << node.second.data_start.size() << endl;
    }
    cout << "status for elem: global" << endl;
    cout << "    max_students: " << max_students << endl;
    cout << "    aver_students: " << all_students / cur_time << endl;

    double time = 0;
    double max_time = 0;
    for (auto i : total_time){
        time += i.second;
        max_time = max(max_time, i.second);
    }
    cout << "    aver_time: " << time / start_time.size() << endl;
    cout << "    max_time: " << max_time << endl;
    return 0;
}
