import React, {Component} from "react";
import EmployeeDataService from "../services/employee.service";
import {Link} from "react-router-dom";
import TreeMenu from "react-simple-tree-menu";
import "react-simple-tree-menu/dist/main.css";
import {flat2Tree} from "../common/utils";

export default class EmployeesList extends Component {
    constructor(props) {
        super(props);
        this.retrieveEmployees = this.retrieveEmployees.bind(this);
        this.refreshList = this.refreshList.bind(this);
        this.setActiveEmployee = this.setActiveEmployee.bind(this);

        this.state = {
            employees: [],
            currentEmployee: null,
        };
    }

    componentDidMount() {
        this.retrieveEmployees();
    }

    retrieveEmployees() {
        EmployeeDataService.getAll()
            .then(response => {
                this.setState({
                    employees: flat2Tree(response.data)
                });
                console.log(response.data);
            })
            .catch(e => {
                console.log(e);
            });
    }

    refreshList() {
        this.retrieveEmployees();
        this.setState({
            currentEmployee: null
        });
    }

    setActiveEmployee(employee) {
        this.setState({
            currentEmployee: employee
        });
    }

    render() {
        const {employees, currentEmployee} = this.state;

        return (
            <div className="row">
                <div className="col-sm-5 col-md-6">
                    <h4>Employees List</h4>

                    <TreeMenu
                        cacheSearch
                        data={employees}
                        onClickItem={({key, label, ...props}) => {
                            this.setActiveEmployee(props);
                        }}
                        debounceTime={125}
                        disableKeyboard={false}
                        hasSearch={false}
                        resetOpenNodesOnDataUpdate={false}
                    >
                    </TreeMenu>
                </div>
                <div className="col-sm-5 col-md-6">
                    {currentEmployee ? (
                        <div>
                            <h4>Employee</h4>
                            <div>
                                <label>
                                    <strong>ID:</strong>
                                </label>{" "}
                                {currentEmployee.id}
                            </div>
                            <div>
                                <label>
                                    <strong>Full Name:</strong>
                                </label>{" "}
                                {`${currentEmployee.first_name} ${currentEmployee.last_name}`}
                            </div>
                            <div>
                                <label>
                                    <strong>Position:</strong>
                                </label>{" "}
                                {currentEmployee.position}
                            </div>
                            <div>
                                <label>
                                    <strong>Hire Date:</strong>
                                </label>{" "}
                                {currentEmployee.hire_date}
                            </div>
                            <div>
                                <label>
                                    <strong>Salary:</strong>
                                </label>{" "}
                                {currentEmployee.salary}
                            </div>

                            <Link
                                to={"/employees/" + currentEmployee.id}
                                className="badge badge-warning"
                            >
                                Edit
                            </Link>
                        </div>
                    ) : (
                        <div>
                            <br/>
                            <p>Please click on a Employee...</p>
                        </div>
                    )}
                </div>
            </div>
        );
    }
}